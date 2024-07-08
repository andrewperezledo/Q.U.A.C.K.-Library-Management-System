from cryptography.fernet import Fernet
from databasekeys import encryptionKey
# need cryptography package for this to work.


def passwordEncrypt(password):

    fernet = Fernet(encryptionKey)

    return fernet.encrypt(password.encode())

def passwordDecrypt(encryptedPassword):

    fernet = Fernet(encryptionKey)

    return fernet.decrypt(encryptedPassword).decode()

