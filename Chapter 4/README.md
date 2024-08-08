# Building AI Intensive Python Applications

## Chapter 4 - Embedding Models

The Python script in this directory uses the `langchain-openai` library to embed textual data with OpenAI's `text-embedding-3-large` model, tailored to produce 1024 dimensional vectors versus 3072, and then the `langchain_mongodb` library to store vectors and execute vector searches.

The example sets up the environment, authenticating to OpenAI with API keys, and connecting to your MongoDB Atlas cluster. Plots for three movies are then embedded and stored in MongoDB Atlas (the vector store) and different vector searches are executed to demonstrate semantic search with ranked results.

### Create MongoDB Atlas cluster

Follow the steps outlined in the MongoDB Atlas [documentation](https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/#procedure) to create your cluster and enable connectivity.

### Create the vector index

To create an Atlas vector search index named `text_vector_index` with the provided index definition, follow these steps:

1. Open your MongoDB Atlas dashboard and navigate to your project.
2. Click on the "Database" tab in the left sidebar, then "Browse Collections".
3. Click "Add my own data" to create an empty database and collection as follows:
* Database name: `embeddings`
* Collection name: `text`
4. Once created, navigate to the "Atlas Search" tab, then click on the "Create Search Index" button.
5. Click "Atlas Vector Search / JSON Editor" and then "Next".
6. Select the "embeddings/text" collection.
7. Enter the Index Name as `text_vector_index`.
8. Replace the vector index JSON definition with this:
```json
{ 
  "fields": [ 
    { 
      "numDimensions": 1024, 
      "path": "embedding", 
      "similarity": "cosine", 
      "type": "vector" 
    } 
  ] 
} 
```
9. Click "Next" and then "Create Search Index".

Now your MongoDB Atlas cluster is set up and ready to be used for storing data with vectors and executing vector searches.

### OpenAI API key and Atlas connection string

Open `semantic_search.py` and add your OpenAI API key and MongoDB Atlas connection string as noted below. You can find the connection string under "Database > Connect" in the Atlas console. Please see the following links for further instructions on obtaining these:
* [Find your OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)
* [Find your MongoDB Atlas connection string](https://www.mongodb.com/docs/guides/atlas/connection-string/)


```
os.environ["OPENAI_API_KEY"] = "<your-openai-api-key>"
ATLAS_CONNECTION_STRING = "<your-connection-string>"
```
Note: Ensure your OpenAI API key has access to the `text-embedding-3-large` model.

### Python libraries and environment

Now you need to setup a Python3 virtual environment and install MongoDB's Python driver, and langchain libraries for OpenAI and MongoDB Atlas Vector Search.

Setup the Python3 virtual environment
```
python3 -m venv myenv
source myenv/bin/activate
```

Once inside the environment (your prompt should show `(myenv)`), install the libraries:
```
pip3 install -r requirements.txt
```

### Execute

You are now ready to execute the script from the virtual environment:

```
python3 semantic_search.py
```

You should see a result like this:

```
(myenv) % python3 semantic_search.py
0
1
2
Documents embedded and inserted successfully.
SEMANTIC QUERY: Secret agent captures underworld boss.
RANKED RESULTS:
[(Document(metadata={'_id': '66aada5537ef2109b3058ccb'}, page_content='A martial artist agrees to spy on a reclusive crime lord using his invitation to a tournament there as cover.'),
  0.770392894744873),
 (Document(metadata={'_id': '66aada5537ef2109b3058ccc'}, page_content='A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.'),
  0.6555435657501221),
 (Document(metadata={'_id': '66aada5537ef2109b3058ccd'}, page_content='When a boy wishes to be big at a magic wish machine, he wakes up the next morning and finds himself in an adult body.'),
  0.5847723484039307)]

SEMANTIC QUERY: Awkward team of space defenders.
RANKED RESULTS:
[(Document(metadata={'_id': '66aada5537ef2109b3058ccc'}, page_content='A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.'),
  0.7871642112731934),
 (Document(metadata={'_id': '66aada5537ef2109b3058ccb'}, page_content='A martial artist agrees to spy on a reclusive crime lord using his invitation to a tournament there as cover.'),
  0.6236412525177002),
 (Document(metadata={'_id': '66aada5537ef2109b3058ccd'}, page_content='When a boy wishes to be big at a magic wish machine, he wakes up the next morning and finds himself in an adult body.'),
  0.5492569208145142)]

SEMANTIC QUERY: A magical tale of growing up.
RANKED RESULTS:
[(Document(metadata={'_id': '66aada5537ef2109b3058ccd'}, page_content='When a boy wishes to be big at a magic wish machine, he wakes up the next morning and finds himself in an adult body.'),
  0.7488957047462463),
 (Document(metadata={'_id': '66aada5537ef2109b3058ccb'}, page_content='A martial artist agrees to spy on a reclusive crime lord using his invitation to a tournament there as cover.'),
  0.5904781222343445),
 (Document(metadata={'_id': '66aada5537ef2109b3058ccc'}, page_content='A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.'),
  0.5809941291809082)]
```

### Conclusion

You've now learned how to perform basic semantic search using an embedding model. Notice that while `text-embedding-3-large` supports up to 3,072 vectors, you can reduce to 1,024 and still obtain a very high quality text embedding.
