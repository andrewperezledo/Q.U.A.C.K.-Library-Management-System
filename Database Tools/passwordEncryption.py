from cryptography.fernet import Fernet
from databasekeys import encryptionKey
# need cryptography package for this to work.


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

