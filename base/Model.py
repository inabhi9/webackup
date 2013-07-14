from app import db
from peewee import *

class BaseModel(db.Model):
    
    def __init__(self, **kwargs):
        super(BaseModel, self).__init__()
        
        for k, v in kwargs.iteritems():
            if isinstance(v, list) and len(v) == 1: v = v[0]
            self.__setattr__(k, v)
    
    def save_conf(self, **kwargs):
        pass

class SourceModel(BaseModel):
    
    class Meta:
        db_table = "source"
    
    id = PrimaryKeyField()
    u_id = IntegerField()
    username = TextField() 
    password = TextField()
    host = TextField()
    port = TextField()
    extra = TextField()
    title = TextField()
    provider = TextField()

class DestinationModel(BaseModel):
    
    class Meta:
        db_table = "destination"
    
    id = PrimaryKeyField()
    u_id = IntegerField()
    username = TextField() 
    password = TextField()
    host = TextField()
    port = TextField()
    extra = TextField()
    title = TextField()
    provider = TextField()

class EventlogModel(BaseModel):
    
    id = PrimaryKeyField()
    type = TextField()
    text = TextField()
    created_at = TextField()
    j_id = IntegerField()
    u_id = IntegerField()
    event = TextField()

    class Meta:
        db_table = "event_log"
