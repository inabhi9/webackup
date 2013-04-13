from peewee import *

from app import db
from base.Model import BaseModel
from flask.ext.login import UserMixin


class UserAuth(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active
    
    def is_active(self):
        return self.active


class User(BaseModel):
    id = PrimaryKeyField()
    username = TextField()
    password = TextField()
    
    def authenticate(self, username, password):        
        user = User.get(User.username == username, User.password == password)
        return user
