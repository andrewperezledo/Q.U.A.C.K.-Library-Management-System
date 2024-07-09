from DatabaseTools.findPost import findPost
from DatabaseTools.updatePost import updatePost
from DatabaseTools.userSearch import userSearch
from DatabaseTools.checkBookAvailability import checkBookAvailability

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


#updatePost("Inventory", "Books", "title", "Harry Potter and the Sorcerer's Stone", "available", True)
#updatePost("Userdata", "Users", "_id", "jimmylynch", "inventory", [])

#print(bookCheckout("Harry Potter and the Sorcerer's Stone", "jimmylynch"))

