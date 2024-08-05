from pymongo import MongoClient

mongoDBaccess = "Insert your access link here."

cluster = MongoClient(mongoDBaccess)

# Set up user section
db = cluster["Userdata"]
collection = db["Users"]

collection.insert_one({"_id": "sample_username", "password": "sample_password",
                       "usertype": "same_type", "books": [],
                       "movies": [], "reservations": [],
                       "history": []})

# Set up books and movies
db = cluster["Inventory"]
collection = db["Books"]

collection.insert_one({'_id': "isbn", 'title': "title",
                       'author': "author", 'release_year': "year",
                       'publisher': "publisher", 'cover_img': "image link",
                       'availability': True, 'due_date': 'none', 'copies': '1',
                       'description': "description", 'genre': "genre",
                       'location': "location", 'version': '1', 'copies_available': 1,
                       'reserved_by': []})

collection = db["Movies"]

collection.insert_one({'_id': 1, 'title': "title",
                       'genre': 'genre',
                       'release_year': 'release_year',
                       'audience_score': "score", 'rotten_score': "score",
                       'gross': "in dollars",
                       'availability': True, 'reserved_by': [],
                       'copies': '1', 'copies_available': 1,
                       'due_date': 'none'
                       })

# Set up events
db = cluster["Events"]
collection = db["Events"]

collection.insert_one({'_id': "YYYY-MM-DD-Period", 'approved': False,
                       "user": "user who created the event", "status": "upcoming",
                       "title": "title", "desc": "desc",
                       "time": "Start time - End time", "contact": "123-456-7890",
                       "attendees": "7"})
