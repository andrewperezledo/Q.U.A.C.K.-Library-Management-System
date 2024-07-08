from pymongo import MongoClient

from databasekeys import cluster

# db and collection are the parameters used to get to desired section of database
# search_parameter and search_value filter which post you will be updating
# new_parameter and new_value are what you are updating
# if there are multiple posts that match the search, only the first post found will update
def updatePost(db, collection, search_parameter, search_value, new_parameter, new_value):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.update_one({search_parameter: search_value}, {"$set":{new_parameter: new_value}})
        print("Post updated.")
    except:
        print("Update failed.")

# updatePost("Inventory","Books","title","Harry Potter and the Sorcerer's Stone","genre","Magic")
