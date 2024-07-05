import pymongo
from bson.json_util import dumps
from pymongo import MongoClient


from databasekeys import cluster

# db and collection are the parameters used to get to desired section of database
# search_parameter and search_value filter which posts you will be updating
# new_parameter and new_value are what you are updating
def updateManyPost(db, collection, search_parameter, search_value, new_parameter, new_value):
    database = cluster[db]
    coll = database[collection]
    try:
        result = coll.update_many({search_parameter: search_value},{"$set": {new_parameter: new_value}})
        print("Posts updated.")
    except pymongo.errors.BulkWriteError as e:
        print(e.details['writeErrors'][0]['errmsg'])


updateManyPost("Inventory","Books",
               "rec_grade", "Middle",
               "genre", "Fantasy")