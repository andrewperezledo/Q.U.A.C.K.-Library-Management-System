import pymongo
from bson.json_util import dumps
from pymongo import MongoClient

from databasekeys import cluster

# db and collection are the parameters used to get to desired section of database
# post is the new item you are adding to the database
# Duplicate _id items fail to add

def addPost(db, collection, post):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.insert_one(post)
        print("Post created.")
    except pymongo.errors.BulkWriteError as e:
        print(e.details['writeErrors'][0]['errmsg'])
        return "writeError"
    except:
        print("Post failed.")


