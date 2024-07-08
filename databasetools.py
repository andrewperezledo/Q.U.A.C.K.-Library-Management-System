import pymongo
from bson.json_util import dumps
from pymongo import MongoClient

from databasekeys import cluster
from userencryption import passwordDecrypt, passwordEncrypt


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


# enter title of book to check out, username is the user who is checking out book
# checks if book exists
# does not have user permission validation, so at this point any user can do this
def bookCheckout(title, username):

    if not checkBookAvailability(title):
        return "Book unavailable"

    data = findPost("Inventory", "Books", "title", title)
    if data is None:
        return "Title does not exist"

    # Sets book to unavailable in inventory system
    updatePost("Inventory", "Books", "title", title, "available", False)
    # Adds book to users profile
    user = userSearch(username)
    if len(user["inventory"]) == 0:
        updatePost("Userdata", "Users", "_id", username, "inventory", [data])
    else:
        inv = user["inventory"]
        inv.append(data)
        updatePost("Userdata", "Users", "_id", username, "inventory", inv)

    return "Book checked out"


# function is designed to check item availability by title
def checkBookAvailability(title):

    data = findPost("Inventory", "Books", "title", title)

    return data["available"]


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


data = findPost("Userdata", "Users","_id","jimmylynch")
for items in data:
    if items == "password":
        print(passwordDecrypt(data[items]))
    else:
        print(data[items])


# enter username
# function returns all user information
def userSearch(username):
    return findPost("Userdata", "Users", "_id", username)


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


if __name__ == "__main__":
    # testing functions
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

    updatePost("Inventory", "Books", "title", "Harry Potter and the Sorcerer's Stone", "available", True)
    updatePost("Userdata", "Users", "_id", "jimmylynch", "inventory", [])

    # print(bookCheckout("Harry Potter and the Sorcerer's Stone", "jimmylynch"))

    checkBookAvailability("Harry Potter and the Order of the Phoenix")

    deleteManyPost("Inventory", "Books", "rec_grade", "Middle")

    deletePost("Inventory", "Books", "_id","978-0590353427")

    print(findManyPost("Inventory", "Books", "genre", "Fanasy"))

    print(loginFunction("jimmylynch","badpassword"))

    updateManyPost("Inventory","Books","genre", "Fantasy","available", True)

    # updatePost("Inventory","Books","title","Harry Potter and the Sorcerer's Stone","genre","Magic")

    print(userCreation("jimmylynch","badpassword","member"))
    
    userSearch("jimmylynch")
