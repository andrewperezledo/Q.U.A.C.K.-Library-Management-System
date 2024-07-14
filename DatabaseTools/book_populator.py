import csv
from databasetools import *
from databasetools import deleteManyPost

import pymongo
from bson.json_util import dumps
from pymongo import MongoClient

from DatabaseTools.databasekeys import cluster
def book_populator():
    count = 0
    print("begin")
    with open('books.csv', mode = 'r')as file:
        csvFile =csv.DictReader(file,delimiter=";")
        for lines in csvFile:
            if count < 120:
                count += 1
                post = {"_id": lines["ISBN"], "title": lines["Book-Title"], "author": lines["Book-Author"], "release_year": lines["Year-Of-Publication"],
                        "publisher": lines["Publisher"], "cover_img": lines["Image-URL-L"], "availability": True}
                print(addPost("Inventory", "Books", post))
            elif count == 0:
                count += 1
            else:
                break



getAllBooks()
