from app import db

class BaseModel(db.Model):
    
    def __init__(self, **kwargs):
        super(BaseModel, self).__init__()
        
        for k, v in kwargs.iteritems():
            if isinstance(v, list) and len(v) == 1: v = v[0]
            self.__setattr__(k, v)
    
    def save_conf(self, **kwargs):
        pass

class SourceModel(BaseModel):
    pass

class DestinationModel(BaseModel):
    pass