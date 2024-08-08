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
Change detected: {'_id': {'_data': '8266B518C6000000012B042C0100296E5A1004CDFFC2D506504F98B11EDBF328641438463C6F7065726174696F6E54797065003C696E736572740046646F63756D656E744B65790046645F6964006466B518C657C4C7204E91E80F000004'}, 'operationType': 'insert', 'clusterTime': Timestamp(1723144390, 1), 'wallTime': datetime.datetime(2024, 8, 8, 19, 13, 10, 112000), 'fullDocument': {'_id': ObjectId('66b518c657c4c7204e91e80f'), 'brand': 'PACKT', 'created': datetime.datetime(2024, 8, 1, 0, 0), 'createdBy': 'jane.smith@packt.com', 'tags': ['Python AI', 'MongoDB Atlas', 'Haystack', 'NLP (Natural Language Processing)', 'Vector Search Integration'], 'revised': datetime.datetime(2024, 8, 10, 0, 0), 'revision': 5, 'title': 'Elevate Your Python AI Projects with MongoDB and Haystack', 'summary': 'MongoDB is excited to announce an integration with Haystack, enhancing MongoDB Atlas Vector Search for Python developers. This integration amplifies our commitment to providing developers with cutting-edge tools for building AI applications centered around semantic search and Large Language Models (LLMs).', 'subscription_type': 'free', 'contributors': [{'type': 'author', 'id': ObjectId('66b39a7fb244729a287708ac')}, {'type': 'editor', 'id': ObjectId('66b39a85b244729a287708ad')}], 'contents': [{'type': 'image', 'id': ObjectId('66b39a8ab244729a287708ae'), 'title': 'python-ai', 'description': 'Atlas Vector Search: Enhance AI development with Haystack.', 'imgUrl': 'https://s3.amazonaws.com/mybucket/images/python-ai-haystack.jpg'}], 'body': {'markup': '<p>Haystack is an open-source Python framework that simplifies AI application development. It enables developers to start their projects quickly, experiment with different AI models, and to efficiently scale their applications...</p>', 'plainText': 'Haystack is an open-source Python framework that simplifies AI application development. It enables developers to start their projects quickly, experiment with different AI models, and to efficiently scale their applications...', 'wordCount': 980}, 'type': 'article'}, 'ns': {'db': 'mdn', 'coll': 'articles'}, 'documentKey': {'_id': ObjectId('66b518c657c4c7204e91e80f')}}. Processing
Updated embeddings for document 66b518c657c4c7204e91e80f
```

After updating [article_1.json](./article_1.json)
```
Change detected: {'_id': {'_data': '8266B518F0000000022B042C0100296E5A1004CDFFC2D506504F98B11EDBF328641438463C6F7065726174696F6E54797065003C7570646174650046646F63756D656E744B65790046645F6964006466B518C657C4C7204E91E80F000004'}, 'operationType': 'update', 'clusterTime': Timestamp(1723144432, 2), 'wallTime': datetime.datetime(2024, 8, 8, 19, 13, 52, 910000), 'fullDocument': {'_id': ObjectId('66b518c657c4c7204e91e80f'), 'brand': 'PACKT', 'created': datetime.datetime(2024, 8, 1, 0, 0), 'createdBy': 'jane.smith@packt.com', 'tags': ['Python AI', 'MongoDB Atlas', 'Haystack', 'NLP (Natural Language Processing)', 'Vector Search Integration'], 'revised': datetime.datetime(2024, 8, 10, 0, 0), 'revision': 5, 'title': 'Elevate Your Python AI Projects with MongoDB and Haystack... NOW!', 'summary': 'MongoDB is extremely excited to announce an integration with Haystack, enhancing MongoDB Atlas Vector Search for Python developers. This integration amplifies our commitment to providing developers with cutting-edge tools for building AI applications centered around semantic search and Large Language Models (LLMs).', 'subscription_type': 'free', 'contributors': [{'type': 'author', 'id': ObjectId('66b39a7fb244729a287708ac')}, {'type': 'editor', 'id': ObjectId('66b39a85b244729a287708ad')}], 'contents': [{'type': 'image', 'id': ObjectId('66b39a8ab244729a287708ae'), 'title': 'python-ai', 'description': 'Atlas Vector Search: Enhance AI development with Haystack.', 'imgUrl': 'https://s3.amazonaws.com/mybucket/images/python-ai-haystack.jpg'}], 'body': {'markup': '<p>Haystack is an open-source Python framework that simplifies AI application development. It enables developers to start their projects quickly, experiment with different AI models, and to efficiently scale their applications...</p>', 'plainText': 'Haystack is an open-source Python framework that simplifies AI application development. It enables developers to start their projects quickly, experiment with different AI models, and to efficiently scale their applications...', 'wordCount': 980}, 'type': 'article', 'semantic_embedding': [-0.0377972275018692, 0.00021847081370651722, ..., -0.005342766176909208]}, 'ns': {'db': 'mdn', 'coll': 'articles'}, 'documentKey': {'_id': ObjectId('66b518c657c4c7204e91e80f')}, 'updateDescription': {'updatedFields': {'summary': 'MongoDB is EXTREMELY excited to announce an integration with Haystack, enhancing MongoDB Atlas Vector Search for Python developers. This integration amplifies our commitment to providing developers with cutting-edge tools for building AI applications centered around semantic search and Large Language Models (LLMs).', 'title': 'Elevate Your Python AI Projects with MongoDB and Haystack... NOW!'}, 'removedFields': [], 'truncatedArrays': []}}. Processing
Updated embeddings for document 66b518c657c4c7204e91e80f
```

### Conclusion

You've now learned how to keep embeddings updated as the field(s) they represent are created or modified. While Change Streams is a battle-tested means of achieving this, they require deployments of their own and the related effort. You may want to consider fully managed options such as [MongoDB Atlas Triggers](https://www.mongodb.com/docs/atlas/app-services/triggers/database-triggers/), the [MongoDB Kafka Sink Connector](https://www.mongodb.com/docs/kafka-connector/current/sink-connector/) or [Atlas Stream Processing](https://www.mongodb.com/docs/atlas/atlas-stream-processing/overview/). 