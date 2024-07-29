import pymongo
from bson.json_util import dumps
from pymongo import MongoClient
from datetime import datetime, timedelta
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
# Updates book in the inventory so that it says unavailable and stores the due date in the inventory page
# as well as inside the users inventory
def bookCheckout(isbn, username):

    data = findPost("Inventory", "Books", "_id", isbn)
    if data is None:
        return "Book does not exist"
    if not data["availability"]:
        return "Book unavailable"

    # Sets book to unavailable in inventory system and assigns due date (3 days from day of checkout)
    updatePost("Inventory", "Books", "_id", isbn, "availability", False)
    data["availability"] = False
    present = datetime.today()
    due = present + timedelta(days=3)
    updatePost("Inventory", "Books", "_id", isbn, "due_date", due)
    data["due_date"] = due
    # Adds book to users profile
    user = userSearch(username)

    if len(user['books']) == 0:
        updatePost("Userdata", "Users", "_id", username, "books", [data])
    else:
        books = user["books"]
        books.append(data)
        updatePost("Userdata", "Users", "_id", username, "books", books)

    return "Book checked out"

def movieCheckout(id_number, username):
    data = findPost("Inventory", "Movies", "_id", id_number)
    if data is None:
        return "Movie does not exist"
    if not data["availability"]:
        return "Movie unavailable"

    # Sets movie to unavailable in inventory system and assigns due date (3 days from day of checkout)
    updatePost("Inventory", "Movies", "_id", id_number, "availability", False)
    data["availability"] = False
    present = datetime.today()
    due = present + timedelta(days=3)
    updatePost("Inventory", "Movies", "_id", id_number, "due_date", due)
    data["due_date"] = due
    # Adds movie to users profile
    user = userSearch(username)

    if len(user['movies']) == 0:
        updatePost("Userdata", "Users", "_id", username, "movies", [data])
    else:
        movies = user["movies"]
        movies.append(data)
        updatePost("Userdata", "Users", "_id", username, "movies", movies)

    return "Movie checked out"


# Example:
# print(bookCheckout("Harry Potter and the Sorcerer's Stone", "jimmylynch"))


# isbn for book to return, username of who is making return
# returns can be soon for each possible case
# "Book returned" indicates success
# Sets book availability to True, due_date to none, and removes book from user inventory
def bookReturn(isbn, username):

    data = findPost("Inventory", "Books", "_id", isbn)
    if data is None:
        return "Book does not exist"

    if data["availability"]:
        return "Book already in-stock"

    updatePost("Inventory", "Books", "_id", isbn, "availability", True)
    updatePost("Inventory", "Books", "_id", isbn, "due_date", "none")

    # Remove book from user profile
    user = userSearch(username)
    new_inventory = user["books"]
    count = 0
    for book in new_inventory:
        if book["_id"] == isbn:
            new_inventory.pop(count)
            break
        count += 1
    updatePost("Userdata", "Users", "_id", username, "books", new_inventory)

    return "Book returned"


def movieReturn(title, username):
    data = findPost("Inventory", "Movies", "title", title)
    if data is None:
        return "Movie does not exist"

    if data["availability"]:
        return "Movie already in-stock"

    updatePost("Inventory", "Movies", "title", title, "availability", True)
    updatePost("Inventory", "Movies", "title", title, "due_date", "none")

    # Remove book from user profile
    user = userSearch(username)
    new_inventory = user["movies"]
    count = 0
    for movie in new_inventory:
        if movie["title"] == title:
            new_inventory.pop(count)
            break
        count += 1
    updatePost("Userdata", "Users", "_id", username, "movies", new_inventory)

    return "Movie returned"

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
        result = coll.update_many({search_parameter: search_value}, {"$set": {new_parameter: new_value}})
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
        coll.update_one({search_parameter: search_value}, {"$set": {new_parameter: new_value}})
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
# Password can't have anything listed in banned characters list.
def userCreation(username, password, usertype):
    banned_characters = ["/", ";", "'", '"', "{", "}", "[", "]", "(", ")", ":"]
    if username == '' or password == '':
        return "Please enter valid username or password."
    for character in password:
        if character in banned_characters:
            return "Please enter valid username or password."
    for character in username:
        if character in banned_characters:
            return "Please enter valid username or password."
    post = {"_id": username, "password": passwordEncrypt(password), "usertype": usertype, "books": []}
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
    results = coll.find({"title": {"$regex": title}})
    for result in results:
        books.append(result)
    return books


# This is the same as book search, except you can fill choose what category to search
# and value is the search key you are looking for
def generalSearch(category, value, type):
    database = cluster['Inventory']
    coll = database[type]
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


time_slots = ["9:00am - 10:00am", "10:30am - 11:30am", "12:00pm - 1:00pm", "1:30pm - 2:30pm", "3:00pm - 4:00pm", "4:30pm - 5:30pm", "6:00pm - 7:00pm"]

# Remove status? Perhaps check time and change status only when event is loaded in?
# When is yyyy-mm-dd-pp, where pp is a period 01-10.
def eventCreation(when, title, desc, contact='', assigned_user='admin', attendees=0, approved=False, status="upcoming"):
    period = time_slots[int(when[len(when)-1])-1]
    post = {"_id": when, "approved": approved, "user": assigned_user, "status": status, "title": title, "desc": desc, "time": period, "contact": contact, "attendees": attendees}
    add = addPost("Events", "Events", post)
    if add == "Duplicate Key":
        return "Time Slot Taken"
    else:
        return add

# Naming syntax leads to other getEventsByPeriod, or getEventsByMonth, etc.
# Date in format yyyy-mm-dd
def getEventsByDate(day):
    events = []
    # Iterates through events of specified date
    for i in range(1, 8):
        post = findPost("Events", "Events", "_id", day + f"-{i}")
        if post and post != "fail" and post["approved"]:
            events.append(post)
        else:
            events.append({"_id": f"{i}", "title": f"{time_slots[i-1]} Available", "time":f"{time_slots[i-1]}"})

    return events


def isSlotAvailable(data):
    post = findPost("Events", "Events", "_id", f"{data["year"]}-{data["month"]}-{data["day"]}-{data["period"]}")
    if post and post != "fail" and post["approved"]:
        return True
    return False


def incrimentRSVP(data):
    post = findPost("Events", "Events", "_id", f"{data["year"]}-{data["month"]}-{data["day"]}-{data["period"]}")
    if post and post != "fail" and post["approved"]:
        attendees = post["attendees"] + 1
        updatePost("Events", "Events", "_id", f"{data["year"]}-{data["month"]}-{data["day"]}-{data["period"]}", "attendees", attendees)
        return True
    return False


def ISBNSearch(isbn, collection):
    database = cluster['Inventory']
    coll = database[collection]
    books = []
    results = coll.find({"_id":isbn})
    for result in results:
        books.append(result)
    return books

# Returns given username's books
def getUserInventory(username):
    user = findPost("Userdata","Users","_id",username)
    return user["books"]


def checkUserOverdue(username):
    user = findPost("Userdata","Users","_id",username)
    present = datetime.today()
    overdue_books = []
    for book in user["books"]:
        if book["due_date"] < present:
            overdue_books.append(book)
    return overdue_books

