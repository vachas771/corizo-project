from flask_pymongo import PyMongo
from flask_login import UserMixin

mongo = PyMongo()

class User(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.id = None  # MongoDB will assign a unique ObjectId

    def save(self):
        mongo.db.users.insert_one({
            'email': self.email,
            'password': self.password
        })

    @classmethod
    def query(cls, filter):
        return mongo.db.users.find(filter)

    @classmethod
    def get_by_id(cls, user_id):
        return mongo.db.users.find_one({'_id': user_id})

class Product:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    @classmethod
    def query(cls):
        return mongo.db.products.find()
