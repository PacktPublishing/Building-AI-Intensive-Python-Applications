# pip3 install PyMongoArrow
import pymongoarrow as pa

import getpass, os, pymongo, pprint

# Extend PyMongo driver with a monkey patch
from pymongoarrow.monkey import patch_all
patch_all()

from datetime import datetime
from pymongo import MongoClient

# Insert some data into MongoDB
client = MongoClient(ATLAS_CONNECTION_STRING)
client.db.data.insert_many([
{'_id': 1, 'amount': 21, 'last_updated': datetime(2020, 12, 10, 1,
3, 1), 'account': {'name': 'Customer1', 'account_number': 1}, 'txns': ['A']},
{'_id': 2, 'amount': 16, 'last_updated': datetime(2020, 7, 23, 6,
7, 11), 'account': {'name': 'Customer2', 'account_number': 2}, 'txns': ['A', 'B']},
{'_id': 3, 'amount': 3, 'last_updated': datetime(2021, 3, 10, 18,
43, 9), 'account': {'name': 'Customer3', 'account_number': 3}, 'txns': ['A', 'B', 'C']},
{'_id': 4, 'amount': 0, 'last_updated': datetime(2021, 2, 25,
3, 50, 31), 'account': {'name': 'Customer4', 'account_number': 4},
'txns': ['A', 'B', 'C', 'D']}])

# create your schema
from pymongoarrow.api import Schema
schema = Schema({'_id': int, 'amount': float, 'last_updated': datetime})

# Perform some find operations
df = client.db.data.find_pandas_all({'amount': {'$gt': 0}}, schema=schema)

arrow_table = client.db.data.find_arrow_all({'amount': {'$gt': 0}}, schema=schema)

df = client.db.data.find_polars_all({'amount': {'$gt': 0}}, schema=schema)

ndarrays = client.db.data.find_numpy_all({'amount': {'$gt': 0}}, schema=schema)

# An example aggregation query
df = client.db.data.aggregate_pandas_all([{'$group': {'_id': None, 'total_ amount': { '$sum': '$amount' }}}])
