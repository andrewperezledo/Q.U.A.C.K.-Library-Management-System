from findPost import findPost


# function is designed to check item availability by title
def checkBookAvailability(title):

    data = findPost("Inventory", "Books", "title", title)

    return data["available"]


checkBookAvailability("Harry Potter and the Order of the Phoenix")
