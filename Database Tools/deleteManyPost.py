import pymongo
from bson.json_util import dumps
from pymongo import MongoClient


from databasekeys import cluster

# db and collection are the parameters used to get to desired section of database
# parameter and value filter which posts you will be deleting


def deleteManyPost(db, collection, parameter, value):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.delete_many({parameter: value})
        print("Posts deleted.")
    except:
        print("Deletion failed.")


deleteManyPost("Inventory", "Books", "rec_grade", "Middle")

