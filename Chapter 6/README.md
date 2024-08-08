# Building AI Intensive Python Applications

## Chapter 6 - AI/ML Application Design

The Python script in this directory (`change_stream.py`) is an implementation of a [MongoDB Change Stream](https://www.mongodb.com/docs/manual/changeStreams/). 

The change stream listens for `insert` operations, or  `update` operations filtered for changes to the `title` and/or `summary` fields of an article. 
 
It then uses `langchain-openai` library to embed the title and summary with OpenAI's `text-embedding-3-large` model, tailored to produce 1024 dimensional vectors versus 3072, and then the `langchain_mongodb` library to store the vector.

### Create MongoDB Atlas cluster

Follow the steps outlined in the MongoDB Atlas [documentation](https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/#procedure) to create your cluster and enable connectivity.

### Create the vector index

To create an Atlas vector search index named `semantic_embedding_vix` with the provided index definition, follow these steps:

1. Open your MongoDB Atlas dashboard and navigate to your project.
2. Click on the "Database" tab in the left sidebar, then "Browse Collections".
3. Click "Add my own data" to create an empty database and collection as follows:
* Database name: `mdn`
* Collection name: `articles`
4. Once created, navigate to the "Atlas Search" tab, then click on the "Create Search Index" button.
5. Click "Atlas Vector Search / JSON Editor" and then "Next".
6. Select the "mdn/articles" collection.
7. Enter the Index Name as `semantic_embedding_vix`.
8. Replace the vector index JSON definition with the contents from [semantic_embedding_vix.json](./mdn_articles__semantic_embedding_vix.json).
9. Click "Next" and then "Create Search Index".

Now your MongoDB Atlas cluster is set up and ready to be used for storing data with vectors and executing vector searches.

### OpenAI API key and Atlas connection string

Open `change_stream.py` and add your OpenAI API key and MongoDB Atlas connection string as noted below. For You can find the connection string under "Database > Connect" in the Atlas console. Please see the following links for further instructions on obtaining these:
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
python3 change_stream.py
```
Using [MongoDB Compass](https://www.mongodb.com/products/tools/compass), [mongosh](https://www.mongodb.com/docs/mongodb-shell/), [mongoimport](https://www.mongodb.com/docs/database-tools/mongoimport/) or the [MongoDB Atlas UI](https://www.mongodb.com/docs/atlas/atlas-ui/documents/), insert the example articles below into the `mdn.articles` collection. The change stream will fire and add the embeddings. Afterwards, try changing the title and/or summary of any of them, and the change stream will re-embedd the changed document(s).

* [article_1.json](./article_1.json)
* [article_2.json](./article_2.json)
* [article_3.json](./article_3.json)

#### Expected output

```
(myenv) % python3 change_stream.py
Listening for changes...
```

After inserting [article_1.json](./article_1.json)
```
Change detected: {'_id': {'_data': '8266B39AA3000000022B042C0100296E5A1004CDFFC2D506504F98B11EDBF328641438463C6F7065726174696F6E54797065003C696E736572740046646F63756D656E744B65790046645F6964006466B39AA3828376D9C0E6A777000004'}, 'operationType': 'insert', 'clusterTime': Timestamp(1723046563, 2), 'wallTime': datetime.datetime(2024, 8, 7, 16, 2, 43, 444000), 'fullDocument': {'_id': ObjectId('66b39aa3828376d9c0e6a777'), 'brand': 'PACKT', 'created': '2024-06-10', 'createdBy': 'jane.smith@packt.com', 'tags': ['Climate', 'sustainability', 'renewable energy', 'solar power'], 'revised': '2022-06-12', 'revision': 5, 'title': 'Solar Energy Advances: Powering the Future', 'summary': 'Exploring the latest innovations in solar technology and their potential impact on sustainable energy solutions.', 'subscription_type': 'free', 'contributors': [{'type': 'author', 'id': ObjectId('66b39a7fb244729a287708ac')}, {'type': 'editor', 'id': ObjectId('66b39a85b244729a287708ad')}], 'contents': [{'type': 'image', 'id': ObjectId('66b39a8ab244729a287708ae'), 'title': 'solar-panels', 'description': 'Innovations in solar panel technology are making renewable energy more efficient and accessible.', 'imgUrl': 'https://s3.amazonaws.com/mybucket/images/solar-energy.jpg'}], 'body': {'markup': '<p>Solar energy is becoming increasingly important in the quest for sustainable energy solutions...</p>', 'plainText': 'Solar energy is becoming increasingly important in the quest for sustainable energy solutions...', 'wordCount': 980}, 'type': 'article'}, 'ns': {'db': 'mdn', 'coll': 'articles'}, 'documentKey': {'_id': ObjectId('66b39aa3828376d9c0e6a777')}}. Processing
Updated embeddings for document 66b39aa3828376d9c0e6a777```
```
After updating [article_1.json](./article_1.json)
```
Change detected: {'_id': {'_data': '8266B39EB6000000022B042C0100296E5A1004CDFFC2D506504F98B11EDBF328641438463C6F7065726174696F6E54797065003C7570646174650046646F63756D656E744B65790046645F6964006466B39AA3828376D9C0E6A777000004'}, 'operationType': 'update', 'clusterTime': Timestamp(1723047606, 2), 'wallTime': datetime.datetime(2024, 8, 7, 16, 20, 6, 467000), 'fullDocument': {'_id': ObjectId('66b39aa3828376d9c0e6a777'), 'brand': 'PACKT',
...
'updateDescription': {'updatedFields': {'summary': 'Exploring the latest innovations in solar technology with AI and their potential impact on sustainable energy solutions.', 'title': 'Solar Energy Advances: Powering the Future with AI'}, 'removedFields': [], 'truncatedArrays': []}}. Processing
Updated embeddings for document 66b39aa3828376d9c0e6a777
```

### Conclusion

You've now learned how to keep embeddings updated as the field(s) they represent are created or modified. While Change Streams is a battle-tested means of achieving this, they require deployments of their own and the related effort. You may want to consider fully managed options such as [MongoDB Atlas Triggers](https://www.mongodb.com/docs/atlas/app-services/triggers/database-triggers/), the [MongoDB Kafka Sink Connector](https://www.mongodb.com/docs/kafka-connector/current/sink-connector/) or [Atlas Stream Processing](https://www.mongodb.com/docs/atlas/atlas-stream-processing/overview/). 