from base.Action import SourceAction
from base.Model import SourceModel
import pymysql
from base import Error
from form import SettingForm
import tarfile, subprocess, json, gzip
from flask.ext.login import current_user

from lib import functions

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
        
        try:
            con = pymysql.connect(
                        db=self.src_ex_db,
                        user=self.src_username,
                        passwd=self.src_password,
                        port=int(self.src_port),
                        host=self.src_host
                    )
        except:
            raise Error.TestConfigException('Could not connect to MySQL server')

    def dump_tar(self):
        fpath = "/tmp/wb_%s.sql.gz" % functions.id_generator(10)
        
        db = '--databases '+self.extra['db'] if self.extra['db'] else '--all-databases'
        passwd = "-p"+self.password if self.password else ''
        cmd = "mysqldump --host %s --port=%s -u %s %s %s" % (self.host, self.port, self.username, passwd, db)
        
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with gzip.open(fpath, "wb") as f:
            f.writelines(p.stdout)

        return fpath