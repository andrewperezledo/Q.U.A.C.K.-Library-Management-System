from pymongo import MongoClient

from databasekeys import mongoDBaccess

cluster = MongoClient(mongoDBaccess)

db = cluster["test"]

collection = db["test"]

post1 = {"_id":30,"name":"jimmy"}
post2 = {"_id":22,"name":"bill"}

results = collection.insert_one(post1)
post_count = collection.count_documents({"_id":23})
print(post_count)