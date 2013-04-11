from peewee import *
from modules import db

class User(db.Model):
    message = TextField()
    created = DateTimeField(default=datetime.datetime.now)