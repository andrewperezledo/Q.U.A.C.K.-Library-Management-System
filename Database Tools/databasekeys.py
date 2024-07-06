from pymongo import MongoClient

mongoDBaccess = "mongodb+srv://jimmylynch03:password@quack.igyfeeo.mongodb.net/?retryWrites=true&w=majority&appName=QUACK"

cluster = MongoClient(mongoDBaccess)
