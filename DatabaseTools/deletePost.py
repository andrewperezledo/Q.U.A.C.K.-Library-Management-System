from pymongo import MongoClient

from DatabaseTools.databasekeys import cluster

# db and collection are the parameters used to get to desired section of database
# parameter and value filter which post you will be deleting

def deletePost(db, collection, parameter, value):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.delete_one({parameter: value})
        print("Post deleted.")
    except:
        print("Deletion failed.")

