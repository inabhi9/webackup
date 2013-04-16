from base.Model import EventlogModel
from model import Profile

def aps_listener(event):
    text = ''
    
    if event.exception:
        rval = Profile().find_by_pk(int(event.job.name.replace('wj_', '')))['profile']
        data = {'type' : 'error', 
                'event': 'scheduled_run', 
                'created_at' : event.scheduled_run_time, 
                'u_id': rval.get('u_id'),
                'j_id':rval.get('id')
        }
        text = '"%s" was failed due to %s' % (rval['title'], event.exception)
        data['text'] = text
    else:
        rval = event.retval
        data = {'type' : 'success', 
                'event': 'scheduled_run', 
                'created_at' : event.scheduled_run_time, 
                'u_id': rval.get('u_id'),
                'j_id':rval.get('id')
        }
        text = '"%s" has been completed successfully' % rval['title']
        data['text'] = text
        
    q = EventlogModel.insert(**data)
    q.execute()
