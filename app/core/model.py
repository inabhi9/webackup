from peewee import *
from app import db

class User(db.Model):
    id = PrimaryKeyField()
    username = TextField()
    password = TextField()
    
    def authenticate(self):
        pass