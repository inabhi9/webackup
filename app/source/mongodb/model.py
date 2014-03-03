from base.Action import SourceAction
from base.Model import SourceModel
import pymysql
from base import Error
from form import SettingForm
import subprocess, json, tarfile, shutil
from flask.ext.login import current_user

from lib import functions
import signal

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
        Check whether MySQL is connecatable
        """
        self._validate(SettingForm)

        username = "-u '" + self.src_username + "'" if self.src_username else ''
        passwd = "-p '" + self.src_password + "'" if self.src_password else ''
        cmd = "mongo --host %s --port %s %s %s --eval exitme" % (self.src_host, self.src_port, username, passwd)

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with p.stdout as r:
            if "couldn't connect to server" in r.read().lower():
                raise Error.TestConfigException('Could not connect to database')
        
    def dump_zipped(self):
        dpath = '/tmp/%s' % functions.id_generator(10)
        fpath = "/tmp/wb_%s.tar.gz" % functions.id_generator(10)
        
        db = '--db ' + self.extra['db'] if self.extra['db'] else ''
        col = '--collection ' + self.extra['coll'] if self.extra['coll'] else ''
        username = "-u '" + self.username + "'" if self.username else ''
        passwd = "-p '" + self.password + "'" if self.password else ''
        cmd = "mongodump --host %s --port %s %s %s %s %s -o %s" % (self.host, self.port, username, passwd, db, col, dpath)

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()

        tar = tarfile.open(fpath, "w:gz")
        tar.add(dpath)
        tar.close()
        
        shutil.rmtree(dpath)
        
        return fpath
