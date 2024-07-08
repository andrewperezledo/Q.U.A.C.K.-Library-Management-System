import pymongo
from bson.json_util import dumps
from pymongo import MongoClient


from DatabaseTools.databasekeys import cluster

# db and collection are the parameters used to get to desired section of database
# posts are the new items you are adding to the database
# Duplicate _id items fail to add

def addManyPost(db, collection, posts):
    database = cluster[db]
    coll = database[collection]
    try:
        result = coll.insert_many(posts, ordered=False)
        print("Posts created.")
    except pymongo.errors.BulkWriteError as e:
        print(e.details['writeErrors'][0]['errmsg'])


post1 = {"_id": "978-0590353427", "title": "Harry Potter and the Sorcerer's Stone", "genre": "Fantasy",
         "rec_grade": "Middle"}
post2 = {"_id": "978-0439064873", "title": "Harry Potter and the Chamber of Secrets", "genre": "Fantasy",
         "rec_grade": "Middle"}
post3 = {"_id": "978-0439136365", "title": "Harry Potter and the Prisoner of Azkaban", "genre": "Fantasy",
         "rec_grade": "Middle"}
post4 = {"_id": "978-0439139601", "title": "Harry Potter and the Goblet of Fire", "genre": "Fantasy",
         "rec_grade": "Middle"}
post5 = {"_id": "978-0439358071", "title": "Harry Potter and the Order of the Phoenix", "genre": "Fantasy",
         "rec_grade": "Middle"}
addManyPost("Inventory", "Books", [post1, post2, post3, post4, post5])


# Try except borrowed from:
# https://stackoverflow.com/questions/44838280/how-to-ignore-duplicate-key-errors-safely-using-insert-many
