from peewee import *
from app import db
from werkzeug import import_string
from base.Model import BaseModel
from flask.ext.login import UserMixin
from base import Error
from flask.ext.login import current_user

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


class Profile(BaseModel):
    
    id = PrimaryKeyField()
    u_id = TextField()
    s_id = IntegerField()
    d_id = IntegerField()
    schedule = TextField()
    compress = IntegerField()
    title = TextField()
    
    def save(self, source, destination, option):
        """ Saving source """
        src_provider = source['src_provider'] + '.model.Source'
        try:
            Source = import_string(src_provider)
        except ValueError:
            raise Error.ProfileException('No source selected')
        except ImportError:
            raise Error.ProfileException('Invalid source')
        
        src = Source(**source)
        s_id = src.save_conf()
        
        """ Saving destination """
        dst_provider = destination['dst_provider'] + '.model.Destination'
        try:
            Destination = import_string(dst_provider)
        except ValueError:
            raise Error.ProfileException('No source selected')
        except ImportError:
            raise Error.ProfileException('Invalid Destination')
        
        dst = Destination(**destination)
        d_id = dst.save_conf()
        
        """ Creating a profile """
        data = {}
        data['u_id'] = current_user.id
        data['s_id'] = s_id
        data['d_id'] = d_id
        data['schedule'] = option['opt_cron']
        data['compress'] = 1 if option['opt_compress'] == 'y' else 'n'
        q = Profile.insert(**data)
        q.execute()