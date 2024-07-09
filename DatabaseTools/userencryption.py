from cryptography.fernet import Fernet
from DatabaseTools.databasekeys import encryptionKey

# password is the basic text password you want to encrypt
# it uses the cryptography package
def passwordEncrypt(password):

    fernet = Fernet(encryptionKey)

    return fernet.encrypt(password.encode())


# password needs to be the fernet.encrypted password, should be a jumble of text
#  it uses the cryptography package
def passwordDecrypt(encryptedPassword):

    fernet = Fernet(encryptionKey)

    return fernet.decrypt(encryptedPassword).decode()