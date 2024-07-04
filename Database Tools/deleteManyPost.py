import pymongo
from bson.json_util import dumps
from pymongo import MongoClient


from databasekeys import cluster


def deleteManyPost(db, collection, parameter, value):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.delete_many({parameter: value})
        print("Posts deleted.")
    except pymongo.errors.BulkWriteError as e:
        print(e.details['writeErrors'])


deleteManyPost("Inventory", "Books", "rec_grade", "Middle")

