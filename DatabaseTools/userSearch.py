from findPost import findPost


# enter username
# function returns all user information
def userSearch(username):
    return findPost("Userdata", "Users", "_id", username)


userSearch("jimmylynch")
