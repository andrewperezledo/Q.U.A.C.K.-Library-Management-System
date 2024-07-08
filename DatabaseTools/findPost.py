from pymongo import MongoClient

from databasekeys import cluster

# db and collection are the parameters used to get to desired section of database
# parameter and value filter which post you are trying to find
# Duplicate _id items fail to add

def findPost(db, collection, parameter, value):
    database = cluster[db]
    coll = database[collection]
    try:
        results = coll.find_one({parameter: value})
        return results
    except:
        return "fail"



