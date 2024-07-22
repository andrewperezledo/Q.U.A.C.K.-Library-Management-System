from pymongo import MongoClient

mongoDBaccess = "mongodb+srv://jimmylynch03:fncaWNzEjcc8AdvA@quack.igyfeeo.mongodb.net/?retryWrites=true&w=majority&appName=QUACK"

# Our database session
cluster = MongoClient(mongoDBaccess)

# Used for password encyrption
encryptionKey = b'aVekEpgaUQJavAoIR7KflJcJUOpHa1GyqoM45BAeyzU='

# Used for session data on app.py
session_secret_key = "Ducks"
