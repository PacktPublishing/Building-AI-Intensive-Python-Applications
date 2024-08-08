import os
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Set the OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = "YOUR-OPENAI-API-KEY"

# Define the MongoDB Atlas connection string 
ATLAS_CONNECTION_STRING = "YOUR-MONGODB_ATLAS-CONNSTRING"

# Create a MongoClient instance to connect to MongoDB Atlas
client = MongoClient(
    ATLAS_CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True
)

# Select the 'articles' collection from the 'mdn' database
coll = client["mdn"]["articles"]

# Instantiate the OpenAIEmbeddings model with specified parameters
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large", dimensions=1024, disallowed_special=()
)


# Define a function to handle changes detected in the MongoDB collection
def handle_changes(change):
    # Extract the document ID from the change event
    doc_id = change["documentKey"]["_id"]

    # Create a filter to identify the document in the collection
    doc_filter = {
        "_id": doc_id
    }  

    # Combine the title and summary of the document into a single text string
    text = [change["fullDocument"]["title"] + " " + change["fullDocument"]["summary"]]

    # Generate embeddings for the text
    embeddings = embedding_model.embed_documents(text)  

    # Create an update document to set the 'semantic_embedding' field with the generated embeddings
    set_fields = {
        "$set": {
            "semantic_embedding": embeddings[0]
        }
    }

    # Update the document in the collection with the new embeddings
    coll.update_one(doc_filter, set_fields)

    print(f"Updated embeddings for document {doc_id}")


# Start monitoring the MongoDB collection for changes
try:
    # Define a stream filter to match insert and update operations affecting the title or summary fields
    stream_filter = [
        {
            "$match": {
                "$or": [
                    {"operationType": "insert"},
                    {
                        "$and": [
                            {"operationType": "update"},
                            {
                                "$or": [
                                    {
                                        "updateDescription.updatedFields.title": {
                                            "$exists": True
                                        }
                                    },
                                    {
                                        "updateDescription.updatedFields.summary": {
                                            "$exists": True
                                        }
                                    },
                                ]
                            },
                        ]
                    },
                ]
            }
        }
    ]

    # Open a change stream to watch for changes in the collection
    with coll.watch(stream_filter, full_document="updateLookup") as stream:
        print("Listening for changes...")
        for change in stream:
            print(f"Change detected: {change}. Processing")
            handle_changes(change)

except PyMongoError as e:
    # Print an error message if a PyMongoError occurs
    print(f"An error occurred: {e}")  

finally:
    # Close the MongoDB client connection
    client.close()  