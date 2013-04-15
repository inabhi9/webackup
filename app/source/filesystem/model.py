import os
from peewee import *
from base.Action import SourceAction
from base.Model import SourceModel
from flask.ext.login import current_user
from base import Error
from lib import functions
import json, tarfile

class Source(SourceModel):
    
    def validate(self):
        SourceAct(**dict(self.__dict__)).test_config()
    
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
        result = os.access(self.src_ex_fs_path, os.R_OK)
        if result == False:
            raise Error.TestConfigException('Directory does not exist or not accessible')
        return result
    
    def dump_tar(self):
        fpath = "/tmp/wb_%s.tar.gz" % functions.id_generator(10)
        
        tar = tarfile.open(fpath, "w:gz")
        tar.add(self.extra['fs_path'])
        tar.close()
        
        return fpath
