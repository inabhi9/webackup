from ftplib import FTP, error_perm
from base.Action import DestinationAction
from base import Error

"""class Source(base.Model.SourceModel):
    pass"""

class DestinationAct(DestinationAction):
    
    def test_config(self):
        """
        Check whether the path user gave has 
        read permission to Application
        """
        ftp = FTP()
        if not self.dst_ftp_path: self.dst_ftp_path = '/rwerwerwe'
        
        """ Testing connection """
        try:
            print ftp.connect(host=self.dst_ftp_host, port=int(self.dst_ftp_port))
        except:
            raise Error.TestConfigException('Could not connect to server')
        
        """  Testing credential """
        try:
            ftp.login(user=self.dst_ftp_username, passwd=self.dst_ftp_password)
        except:
            raise Error.TestConfigException('Could not log in')
        
        """ Testing path """
        try:
            print ftp.cwd(self.dst_ftp_path)
        except:
            raise Error.TestConfigException('"%s" directory does not exists' % self.dst_ftp_path)
        
        """ Testing write permission """
        try:
            ftp.mkd(self.dst_ftp_path + '/wrtest98494')
        except error_perm, e:
            if str(e)=="550 Target exist.": return
            raise Error.TestConfigException('"%s" directory is not writable' % self.dst_ftp_path)
        finally:
            ftp.rmd(self.dst_ftp_path + '/wrtest98494')
        