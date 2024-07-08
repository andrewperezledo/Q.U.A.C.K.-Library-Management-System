from addPost import addPost
from findPost import findPost
from passwordEncryption import passwordEncrypt
from passwordEncryption import passwordDecrypt


def userCreation(username, password, usertype):
    post = {"_id": username, "password": passwordEncrypt(password), "usertype": usertype}
    add = addPost("Userdata", "Users", post)
    if(add == "writeError"):
        print("Matching Username")


userCreation("jimmylynch","badpassword","member")

data = findPost("Userdata", "Users","_id","jimmylynch")
for items in data:
    if items == "password":
        print(passwordDecrypt(data[items]))
    else:
        print(data[items])