from pymongo import MongoClient

from databasekeys import cluster


def deletePost(db, collection, parameter, value):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.delete_one({parameter: value})
        print("Post deleted.")
    except:
        print("Deletion failed.")


deletePost("Inventory", "Books", "_id","978-0590353427")
