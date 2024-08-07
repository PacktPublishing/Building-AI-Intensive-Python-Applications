# Building AI Intensive Python Applications
# Chapter 4 - Embedding Models

# Requires: langchain, langchain-mongodb, langchain-openai, pymongo
# Requires: virtualenv, python3, pip3
# Requires: OpenAI API key with access to "text-embedding-3-large" model
# Requires: MongoDB Atlas cluster with vector index created

# Setup:
# python3 -m venv myenv
# source myenv/bin/activate
# pip3 install --upgrade --quiet pythondns langchain langchain-community langchain-mongodb langchain-openai pymongo

# Usage:
# python3 semantic_search.py

import os
import pprint
import time
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient

os.environ["OPENAI_API_KEY"] = "<your-openai-api-key>"
ATLAS_CONNECTION_STRING = "<your-connection-string>"

client = MongoClient(
    ATLAS_CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True
)

db_name = "embeddings"
collection_name = "text"
coll = client[db_name][collection_name]
vector_search_index = "text_vector_index"

coll.delete_many({})

texts = []
texts.append(
    "A martial artist agrees to spy on a reclusive crime lord using his invitation to a tournament there as cover."
)
texts.append(
    "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."
)
texts.append(
    "When a boy wishes to be big at a magic wish machine, he wakes up the next morning and finds himself in an adult body."
)

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large", dimensions=1024, disallowed_special=()
)

embeddings = embedding_model.embed_documents(texts)

docs = []
for i in range(len(texts)):
    print(i)
    docs.append({"text": texts[i], "embedding": embeddings[i]})

coll.insert_many(docs)
print("Documents embedded and inserted successfully.")

time.sleep(3)  # allow vector store to undergo indexing

semantic_queries = []
semantic_queries.append("Secret agent captures underworld boss.")
semantic_queries.append("Awkward team of space defenders.")
semantic_queries.append("A magical tale of growing up.")

vector_search = MongoDBAtlasVectorSearch(
    collection=coll,
    embedding=OpenAIEmbeddings(
        model="text-embedding-3-large", dimensions=1024, disallowed_special=()
    ),
    index_name=vector_search_index,
)

for q in semantic_queries:
    results = vector_search.similarity_search_with_score(query=q, k=3)
    print("SEMANTIC QUERY: " + q)
    print("RANKED RESULTS: ")
    pprint.pprint(results)
    print("")
