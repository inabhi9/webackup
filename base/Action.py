
class SourceAction(object):
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if isinstance(v, list) and len(v) == 1: v = v[0]
            self.__setattr__(k, v)
    
    def auth(self, **kwargs):
        pass
    
    def test_config(self):
        raise NotImplementedError( "Should have implemented this" )
    
    def get_auth(self):
        pass
    
    def dump(self, **kwargs):
        pass
    
    def dump_tar(self, **kwargs):
        pass
    
    def ncftpput_string(self, **kwargs):
        pass



class DestinationAction(object):
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if isinstance(v, list) and len(v) == 1: v = v[0]
            self.__setattr__(k, v)
    
    def test_config(self):
        raise NotImplementedError( "Should have implemented this" )