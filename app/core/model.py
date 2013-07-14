from peewee import *
from app import db
from werkzeug import import_string
from base.Model import BaseModel, DestinationModel, SourceModel, EventlogModel
from flask.ext.login import UserMixin
from base import Error
from flask.ext.login import current_user
import json, subprocess, os
from lib import functions
from datetime import datetime

class UserAuth(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active
    
    def is_active(self):
        return self.active


class User(BaseModel):
    id = PrimaryKeyField()
    username = TextField()
    password = TextField()
    
    def authenticate(self, username, password):        
        user = User.get(User.username == username, User.password == password)
        return user


class Profile(BaseModel):
    
    id = PrimaryKeyField()
    u_id = TextField()
    s_id = IntegerField()
    d_id = IntegerField()
    cron = TextField()
    title = TextField()
    email_notify = IntegerField()
    compress = IntegerField()
    split_size = IntegerField()
    
    def create(self, source, destination, option):
        
        """ Selecting source """
        src_provider = source['src_provider'] + '.model.Source'
        try:
            Source = import_string(src_provider)
            src = Source(**source)
        except ValueError:
            raise Error.ProfileException('No source selected')
        except ImportError:
            raise Error.ProfileException('Invalid source')
        
        """ Selecting destination """
        dst_provider = destination['dst_provider'] + '.model.Destination'
        try:
            Destination = import_string(dst_provider)
            dst = Destination(**destination)
        except ValueError:
            raise Error.ProfileException('No destination selected')
        except ImportError:
            raise Error.ProfileException('Invalid Destination')
        
        """ Validation """
        src.validate()
        dst.validate()
        
        """ Saving """
        s_id = src.save_conf()
        d_id = dst.save_conf()
        
        """ Creating a profile """
        data = {}
        data['u_id'] = current_user.id
        data['s_id'] = s_id
        data['d_id'] = d_id

        for k, v in option.iteritems():
            data[k.replace('opt_', '')] = v
        
        data['compress'] = 1 if 'opt_compress' in option else 0
        data['email_notify'] = 1 if 'opt_email_notify' in option else 0
        
        q = Profile.insert(**data)
        return q.execute()
        
    def retrieve(self, **kwargs):
        jobs = kwargs.get('jobs', [])
        jobs_dict = {}
        for j in jobs:
            jobs_dict[j.name.replace('wj_', '')] = j

        u_id = current_user.id
        
        sq = Profile.select().where(Profile.u_id == u_id)
        qr = sq.execute()
        
        data = []
        for r in qr:
            if jobs_dict.get(str(r.id)):
                r._data['status'] = 1
            else:
                r._data['status'] = 0
            
            try:    
                qe = EventlogModel.select().where(EventlogModel.j_id == r._data['id']).order_by(EventlogModel.id.desc()).limit(1)
                for res in qe.execute():
                    r._data['last_execute'] = res._data['created_at']
            except:
                pass
            
            data.append(r._data)
            
        return data
    
    def find_by_pk(self, p_id):
        profile = Profile.get(Profile.id == p_id)
        p = profile._data
        
        sched = {}
        c = profile.cron.split(' ')
        sched['minute'] = c[0]
        sched['hour'] = c[1]
        sched['day'] = c[2]
        sched['month'] = c[3]
        sched['day_of_week'] = c[4]
        
        s = SourceModel.get(SourceModel.id == profile.s_id)
        s._data['extra'] = json.loads(s._data['extra'])
        s = s._data
        
        d = DestinationModel.get(DestinationModel.id == profile.d_id)
        d._data['extra'] = json.loads(d._data['extra'])
        d = d._data
        
        
        return {'profile': p, 'source' : s, 'destination' : d, 'cron' : sched}
    
    def delete_by_pk(self, p_id):
        profile = Profile.get(Profile.id == p_id)
        source = SourceModel.get(SourceModel.id == profile.s_id)
        destination = DestinationModel.get(DestinationModel.id == profile.d_id)
        
        profile.delete_instance()
        source.delete_instance()
        destination.delete_instance()


class Eventlog(EventlogModel):
    
    def retrieve(self, **kwargs):
        jobs = kwargs.get('jobs', [])
        jobs_dict = {}
        for j in jobs:
            jobs_dict[j.name.replace('wj_', '')] = j
    
        u_id = current_user.id
        
        sq = EventlogModel.select().where(EventlogModel.u_id == u_id).order_by(EventlogModel.id.desc())
        qr = sq.execute()
        
        data = []
        for r in qr:
            data.append(r._data)
            
        return data
    
    def remove_all(self, u_id):
        delete_query = EventlogModel.delete().where(EventlogModel.u_id == u_id)
        delete_query.execute()

def profile_execute(p_id):
    data = Profile().find_by_pk(p_id)
    source = data['source']
    destination = data['destination']
    data = data['profile']
    split = int(data.get('split_size') or 0)
    
    """ Dumping from Source """
    SourceAct = import_string(source.get('provider') + '.model.SourceAct')
    src_act = SourceAct(**source)
    file_name = src_act.dump_zipped()
    
    """ Output file name """
    dt_utc = datetime.utcnow().strftime('%Y_%m_%d_%H-%M-%S')
    out = 'wb_' + functions.clean_str(data['title']) + dt_utc + functions.ext_file(file_name)
    
    if split > 0:
        cmd = "split -b %sm %s /tmp/%s" % (split, file_name, out)
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    """ Executing destination part  """
    DestinationAct = import_string(destination.get('provider') + '.model.DestinationAct')
    dst_act = DestinationAct(**destination)
    if split == 0:
        dst_act.upload_file(file_name, out)
    elif split > 0:
        dst_act.mkdir(dt_utc)
        dst_act.cd(dt_utc)
        for f in os.listdir('/tmp'):
            if f.startswith(out):
                dst_act.upload_file('/tmp/%s' % f, f)
        os.unlink(file_name)
    
    return data
