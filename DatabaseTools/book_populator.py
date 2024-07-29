import csv
from datetime import datetime, timedelta
from databasetools import *
from databasetools import deleteManyPost

import pymongo
from bson.json_util import dumps
from pymongo import MongoClient

from DatabaseTools.databasekeys import cluster


def book_populator():
    count = 0
    print("begin")
    with open('movies.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        for lines in csvFile:
            if count < 120:
                count += 1
                post = {"_id": count, "title": lines["Film"], "genre": lines["Genre"], "release_year": lines["Year"],
                        "audience_score": lines["Audience score %"], "rotten_score": lines["Rotten Tomatoes %"],
                        "gross": lines["Worldwide Gross"], "availability": True}
                print(addPost("Inventory", "Movies", post))
            elif count == 0:
                count += 1
            else:
                break


def book_updater():
    db = cluster["Inventory"]
    collection = db["Books"]
    collection.update_many({"due_date": {"$exists": False}}, {"$set": {"due_date": "none"}})


# print(bookCheckout("0195153448","jimmy"))
# data = checkUserOverdue("jimmy")
# for book in data:
#     print(book)

db = cluster["Inventory"]
collection = db["Movies"]
collection.update_many({"reservation_queue": {"$exists": False}}, {"$set": {"reservation_queue": []}})

#movieCheckout("Zack and Miri Make a Porno","jimmy")
#movieReturn("WALL-E","member")
#checkUserOverdue()





