import pymongo
from bson.json_util import dumps
from pymongo import MongoClient

from DatabaseTools.databasekeys import cluster
from DatabaseTools.userencryption import passwordDecrypt, passwordEncrypt


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
# Example:
# post1 = {"_id": "978-0590353427", "title": "Harry Potter and the Sorcerer's Stone", "genre": "Fantasy",
#      "rec_grade": "Middle"}
# post2 = {"_id": "978-0439064873", "title": "Harry Potter and the Chamber of Secrets", "genre": "Fantasy",
#         "rec_grade": "Middle"}
# post3 = {"_id": "978-0439136365", "title": "Harry Potter and the Prisoner of Azkaban", "genre": "Fantasy",
#         "rec_grade": "Middle"}
# post4 = {"_id": "978-0439139601", "title": "Harry Potter and the Goblet of Fire", "genre": "Fantasy",
#         "rec_grade": "Middle"}
# post5 = {"_id": "978-0439358071", "title": "Harry Potter and the Order of the Phoenix", "genre": "Fantasy",
#         "rec_grade": "Middle"}

# addManyPost("Inventory", "Books", [post1, post2, post3, post4, post5])


# Try except borrowed:
# https://stackoverflow.com/questions/44838280/how-to-ignore-duplicate-key-errors-safely-using-insert-many

# db and collection are the parameters used to get to desired section of database
# post is the new item you are adding to the database
# Duplicate _id items fail to add
def addPost(db, collection, post):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.insert_one(post)
        return "success"
    except pymongo.errors.DuplicateKeyError as e:
        return "Duplicate Key"
    except:
        return "fail"


# enter isbn of book to check out, username is the user who is checking out book
# checks if book exists
# does not have user permission validation, so at this point any user can do this
def bookCheckout(isbn, username):

    if not checkBookAvailability(isbn):
        return "Book unavailable"

    data = findPost("Inventory", "Books", "_id", isbn)
    if data is None:
        return "Book does not exist"

    # Sets book to unavailable in inventory system
    updatePost("Inventory", "Books", "_id", isbn, "availability", False)
    # Adds book to users profile
    user = userSearch(username)

    try:
        if len(user["books"]) == 0:
            updatePost("Userdata", "Users", "_id", username, "books", [data])
        else:
            books = user["books"]
            books.append(data)
            updatePost("Userdata", "Users", "_id", username, "books", books)
    except:
        #TODO
        # make book inventory array
        # add books field for user 
        updatePost("Userdata", "Users", "_id", username, "books", [data])

    return "Book checked out"
# Example:
# print(bookCheckout("Harry Potter and the Sorcerer's Stone", "jimmylynch"))


# function is designed to check item availability by title
def checkBookAvailability(isbn):

    data = findPost("Inventory", "Books", "_id", isbn)

    return data["availability"]
# Example:
# checkBookAvailability("Harry Potter and the Order of the Phoenix")


# db and collection are the parameters used to get to desired section of database
# parameter and value filter which posts you will be deleting
def deleteManyPost(db, collection, parameter, value):
    database = cluster[db]
    coll = database[collection]
    try:
        coll.delete_many({parameter: value})
        print("Posts deleted.")
    except:
        print("Deletion failed.")
# Example:
# deleteManyPost("Inventory", "Books", "rec_grade", "Middle")


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
# Example:
# deletePost("Inventory", "Books", "_id","978-0590353427")


# db and collection are the parameters used to get to desired section of database
# parameter and value filter which posts you are searching for
# Returns empty vector if no results are found
def findManyPost(db, collection, parameter, value):
    database = cluster[db]
    coll = database[collection]
    try:
        results = coll.find({parameter: value})
        print("Search success.")
        data = []
        for result in results:
            data.append(result)
        return data
    except:
        print("Search failed.")
# Example:
# print(findManyPost("Inventory", "Books", "genre", "Fanasy"))


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
# Example:
# data = findPost("Userdata", "Users","_id","jimmylynch")
# for items in data:
#     if items == "password":
#         print(passwordDecrypt(data[items]))
#     else:
#         print(data[items])


# db and collection are the parameters used to get to desired section of database
# search_parameter and search_value filter which posts you will be updating
# new_parameter and new_value are what you are updating
def updateManyPost(db, collection, search_parameter, search_value, new_parameter, new_value):
    database = cluster[db]
    coll = database[collection]
    try:
        result = coll.update_many({search_parameter: search_value},{"$set": {new_parameter: new_value}})
        print("Posts updated.")
    except:
        print("Update failed.")
# Example:
# updateManyPost("Inventory","Books","genre", "Fantasy","available", True)


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
# Example:
# updatePost("Inventory", "Books", "title", "Harry Potter and the Sorcerer's Stone", "available", True)
# updatePost("Userdata", "Users", "_id", "jimmylynch", "inventory", [])
# updatePost("Inventory","Books","title","Harry Potter and the Sorcerer's Stone","genre","Magic")


# username is the username, must be unique
# password is password, will get encrypted
# usertype should be either member, employee, or admin and will be used to enable account features
def userCreation(username, password, usertype):
    post = {"_id": username, "password": passwordEncrypt(password), "usertype": usertype}
    add = addPost("Userdata", "Users", post)
    if add == "Duplicate Key":
        return "Matching Username"
    else:
        return add
# Example:
# print(userCreation("jimmylynch","badpassword","member"))


# enter username
# function returns all user information
def userSearch(username):
    return findPost("Userdata", "Users", "_id", username)
# Example:
# userSearch("jimmylynch")


# enter username and password
# function decrypts password and checks if user exists
# returns either login successful or message stating incorrect parameters
def loginFunction(username, password):

    results = findPost("Userdata", "Users", "_id", username)
    if results is None:
        return "Username or Password is incorrect."

    decpassword = passwordDecrypt(results["password"])
    if (results["_id"] == username) and (password == decpassword):
        return "Login Successful."
    else:
        return "Username or Password is incorrect."
# Example:
# print(loginFunction("jimmylynch","badpassword"))

def getAllBooks():
    database = cluster['Inventory']
    coll = database['Books']
    books = []
    results = coll.find({})
    for result in results:
        books.append(result)
    return books

def bookSearch(title):
    database = cluster['Inventory']
    coll = database['Books']
    books = []
    results = coll.find({"title":{"$regex":title}})
    for result in results:
        books.append(result)
    return books

# This is the same as book search, except you can fill choose what category to search
# and value is the search key you are looking for
def generalSearch(category,value):
    database = cluster['Inventory']
    coll = database['Books']
    books = []
    results = coll.find({category: {"$regex": value}})
    for result in results:
        books.append(result)
    return books

def getAllUsers():
    database = cluster['Userdata']
    coll = database['Users']
    users = list(coll.find({}, {'_id': 1, 'usertype': 1}))
    return [{'username': user['_id'], 'usertype': user['usertype']} for user in users]

def updateUserRole(username, new_role):
    database = cluster['Userdata']
    coll = database['Users']
    result = coll.update_one({'_id': username}, {'$set': {'usertype': new_role}})
    return result.modified_count > 0
    
# Remove status? Perhaps check time and change status only when event is loaded in?
# When is yyyy-mm-dd-pp, where pp is a period 01-10.
def eventCreation(when, title, desc, contact = '', approved=False, status = "upcoming"):
    post = {"_id": when, "approved": approved, "status":status, "title": title, "desc": desc, "contact": contact}
    add = addPost("Events", "Events", post)
    if add == "Duplicate Key":
        return "Time Slot Taken"
    else:
        return add
    
# Naming syntax leads to other getEventsByPeriod, or getEventsByMonth, etc.
# Date in format yyyy-mm-dd
def getEventsByDate(day):
    # database = cluster["Events"]
    # coll = database["Events"]

    users = []
    # Iterates through events of specified date
    for i in range(1, 11):
        post = findPost("Events", "Events", "_id", day + f"-{i:02d}")
        if post and post != "fail":
            users.append(post)

    return users

def ISBNSearch(isbn):
    database = cluster['Inventory']
    coll = database['Books']
    books = []
    results = coll.find({"_id":{"$regex":isbn}})
    for result in results:
        books.append(result)
    return books
