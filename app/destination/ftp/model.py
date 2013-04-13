from ftplib import FTP
from base.Action import SourceAction

"""class Source(base.Model.SourceModel):
    pass"""

class SourceAct(SourceAction):
    
    def test_config(self):
        """
        Check whether the path user gave has 
        read permission to Application
        """
        ftp = FTP(host=self.src_ftp_host,
                  user=self.src_ftp_username,
                  passwd=self.src_ftp_password)
