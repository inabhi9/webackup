import os
from base.Action import SourceAction

"""class Source(base.Model.SourceModel):
    pass"""

class SourceAct(SourceAction):
    
    def test_config(self):
        """
        Check whether the path user gave has 
        read permission to Application
        """
        return os.access(self.src_fs_path, os.R_OK)