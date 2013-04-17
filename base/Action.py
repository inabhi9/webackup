import Error


class SourceAction(object):
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if isinstance(v, list) and len(v) == 1: v = v[0]
            self.__setattr__(k, v)
    
    def auth(self, **kwargs):
        pass
    
    def test_config(self):
        raise NotImplementedError("Should have implemented this")
    
    def get_auth(self):
        pass
    
    def dump(self, **kwargs):
        pass
    
    def dump_tar(self, **kwargs):
        pass
    
    def ncftpput_string(self, **kwargs):
        pass
    
    def _validate(self, setting_form):
        f = setting_form(**self.__dict__)
        f.validate()
        for field, errors in f.errors.items():
            for error in errors:
                raise Error.ValidationException("Error in the %s field - %s" % (getattr(f, field).label.text, error))


class DestinationAction(object):
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if isinstance(v, list) and len(v) == 1: v = v[0]
            self.__setattr__(k, v)
    
    def test_config(self):
        raise NotImplementedError("Should have implemented this")
    
    def upload_file(self, file_name):
        raise NotImplementedError("Should have implemented this")
