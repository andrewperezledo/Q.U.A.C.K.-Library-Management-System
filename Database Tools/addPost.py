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
    except:
        print("Post failed.")


post = {"_id": "978-0590353427", "title": "Harry Potter and the Sorcerer's Stone", "genre": "Fantasy",
         "rec_grade": "Middle"}

addPost("Inventory", "Books", post)
