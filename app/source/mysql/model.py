from base.Action import SourceAction
from base.Model import SourceModel
import pymysql
from base import Error
from form import SettingForm

class Source(SourceModel):
    pass

class SourceAct(SourceAction):
    
    def test_config(self):
        """
        Check whether MySQL is connecatable
        """
        self._validate(SettingForm)
        
        try:
            con = pymysql.connect(
                        db=self.src_db,
                        user=self.src_username,
                        passwd=self.src_password,
                        port=int(self.src_port),
                        host=self.src_host
                    )
        except:
            raise Error.TestConfigException('Could not connect to MySQL server')
