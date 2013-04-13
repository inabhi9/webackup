from base.Action import SourceAction
from peewee import MySQLDatabase

"""class Source(base.Model.SourceModel):
    pass"""

class SourceAct(SourceAction):
    
    def test_config(self):
        """
        Check whether MySQL is connecatable
        """
        
        mysql_db = MySQLDatabase(self.src_msql_db,
                                 user=self.src_msql_username,
                                 passwd=self.src_msql_password,
                                 port=int(self.src_msql_port),
                                 host=self.src_msql_host)
        try:
            mysql_db.connect()
            return True
        except:
            return False
