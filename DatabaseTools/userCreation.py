from DatabaseTools.addPost import addPost
from DatabaseTools.findPost import findPost
from DatabaseTools.passwordEncryption import passwordEncrypt
from DatabaseTools.passwordEncryption import passwordDecrypt



# username is the username, must be unique
# password is password, will get encrypted
# usertype should be either member, employee, or admin and will be used to enable account features
#
def userCreation(username, password, usertype):
    post = {"_id": username, "password": passwordEncrypt(password), "usertype": usertype}
    add = addPost("Userdata", "Users", post)
    if add == "Duplicate Key":
        return "Matching Username"
    else:
        return add

