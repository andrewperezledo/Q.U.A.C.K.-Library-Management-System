from addPost import addPost
from findPost import findPost
from passwordEncryption import passwordEncrypt
from passwordEncryption import passwordDecrypt



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


print(userCreation("jimmylynch","badpassword","member"))


data = findPost("Userdata", "Users","_id","jimmylynch")
for items in data:
    if items == "password":
        print(passwordDecrypt(data[items]))
    else:
        print(data[items])
