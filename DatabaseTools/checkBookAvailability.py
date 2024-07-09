from DatabaseTools.findPost import findPost


# function is designed to check item availability by title
def checkBookAvailability(title):

    data = findPost("Inventory", "Books", "title", title)

    return data["available"]


