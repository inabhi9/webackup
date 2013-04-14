import os
from peewee import *
from base.Action import SourceAction
from base.Model import SourceModel
from flask.ext.login import current_user
from base import Error
import json


class Source(SourceModel):
    
    id = PrimaryKeyField()
    u_id = IntegerField()
    username = TextField() 
    password = TextField()
    host = TextField()
    port = TextField()
    extra = TextField()
    title = TextField()
    provider = TextField()
    
    def save_conf(self):
        data = {}
        extra = {}
        for k, v in dict(self.__dict__).iteritems():
            if k.startswith('src_ex_'):
                extra[k.replace('src_ex_', '')] = v
            elif k.startswith('src_'):
                data[k.replace('src_', '')] = v

        extra = json.dumps(extra)
        data['extra'] = extra
        data['u_id'] = current_user.id
        
        q = Source.insert(**data)
        nid = q.execute()
        if not nid:
            raise Error.ProfileException
        
        return nid

class SourceAct(SourceAction):
    
    def test_config(self):
        """
        Check whether the path user gave has 
        read permission to Application
        """
        return os.access(self.src_ex_fs_path, os.R_OK)