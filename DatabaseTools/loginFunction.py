from findPost import findPost
from passwordEncryption import passwordDecrypt


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


print(loginFunction("jimmylynch","badpassword"))