from peewee import *
from ftplib import FTP, error_perm
from base.Action import DestinationAction
from base.Model import DestinationModel
from base import Error
from flask.ext.login import current_user
import json, os
from datetime import datetime
 
class Destination(DestinationModel):
        
    def validate(self):
        DestinationAct(**dict(self.__dict__)).test_config()    
    
    def save_conf(self):
        data = {}
        extra = {}
        for k, v in dict(self.__dict__).iteritems():
            if k.startswith('dst_ex_'):
                extra[k.replace('dst_ex_', '')] = v
            elif k.startswith('dst_'):
                data[k.replace('dst_', '')] = v

        extra = json.dumps(extra)
        data['extra'] = extra
        data['u_id'] = current_user.id
        
        q = Destination.insert(**data)
        nid = q.execute()
        if not nid:
            raise Error.ProfileException
        
        return nid
            

class DestinationAct(DestinationAction):
    
    def test_config(self):
        """
        Check whether the path user gave has 
        read permission to Application
        """
        ftp = FTP()
        if not self.dst_ex_path: self.dst_ex_path = '/'
        
        """ Testing connection """
        try:
            print ftp.connect(host=self.dst_host, port=int(self.dst_port))
        except:
            raise Error.TestConfigException('Could not connect to server')
        
        """  Testing credential """
        try:
            ftp.login(user=self.dst_username, passwd=self.dst_password)
        except:
            raise Error.TestConfigException('Could not log in')
        
        """ Testing path """
        try:
            print ftp.cwd(self.dst_ex_path)
        except:
            raise Error.TestConfigException('"%s" directory does not exists' % self.dst_ex_path)
        
        """ Testing write permission """
        try:
            ftp.mkd(self.dst_ex_path + '/wr98494test')
        except error_perm, e:
            if str(e)=="550 Target exist.": return
            raise Error.TestConfigException('"%s" directory is not writable' % self.dst_ex_path)
        finally:
            ftp.rmd(self.dst_ex_path + '/wr98494test')

    def upload_file(self, file_name):
        fnm, fext = os.path.splitext(file_name)
        fnm = datetime.utcnow().strftime('webackup_%Y_%m_%d_%H-%M-%S')
        if fext == '.gz': fext = '.tar.gz'
        
        ftp = FTP()
        ftp.connect(host=self.host, port=int(self.port))
        ftp.login(user=self.username, passwd=self.password)
        ftp.cwd(self.extra['path'])
        ftp.storbinary("STOR %s%s" % (fnm, fext), open(file_name, "rb"))
        
        os.unlink(file_name)
        