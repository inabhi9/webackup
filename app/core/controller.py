from flask import Blueprint, render_template, request, redirect, flash
from flask.ext.login import login_user, login_required, logout_user
import form
from base import Error
from lib import resp_format
from peewee import DoesNotExist
from model import User, UserAuth, Profile, profile_execute
from app import SOURCES, DESTINATIONS, login_manager, sched

register = Blueprint('core', __name__,
                     template_folder='templates')


@login_manager.user_loader
def load_user(id):
    usr = User.get(User.id == id)
    return UserAuth(usr.username, usr.id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@register.route('/login', methods=['GET', 'POST'])
def login():
    login_form = form.LoginForm()
    if request.method == 'POST':
        try:
            user = User().authenticate(request.form['field_username'], request.form['field_password'])
            login_user(UserAuth(user.username, user.id))
            return redirect('/')
        except DoesNotExist:
            flash('Invalid username or password', 'error')
        
    return render_template('login.html', form=login_form)

@register.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@register.route('/')
@login_required
def index():
    form_opt = form.OptionForm()
    return render_template('index.html',
                           sources=SOURCES,
                           destinations=DESTINATIONS,
                           form_opt=form_opt)

@register.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    if request.method == 'GET':
        return profile_list()
    
    try:
        s = {}; d = {}; o = {}
        for k, v in request.form.iteritems():
            if k.startswith('src_'):
                s[k] = v
            elif k.startswith('dst_'):
                d[k] = v
            elif k.startswith('opt_'):
                o[k] = v

        p_id = Profile().create(s, d, o)
        p, s, d, c = Profile().find_by_pk(p_id)
        sched.add_cron_job(profile_execute, args=[p, s, d], name='wj_%s' % p_id, **c)
        
        return resp_format.from_dict(resp_format.MSG_OK, msg='Profile successfully created')
    except Error.ProfileException as e:
        return resp_format.from_dict(resp_format.MSG_FAIL, msg=str(e))
    except Error.TestConfigException as e:
        return resp_format.from_dict(resp_format.MSG_FAIL, msg=str(e))

def profile_list():
    data = Profile().retrieve(jobs=sched.get_jobs())
    return render_template('profile.html', profiles=data)

def delete_profile():
    pass

@register.route('/core/list')
@login_required
def lists():
    if request.args.get('type') == 'source':
        return render_template('_source_list.html', sources=SOURCES)
    elif request.args.get('type') == 'destination':
        return render_template('_destination_list.html', destinations=DESTINATIONS)

@register.route('/core/dryrun')
@login_required
def dryrun():
    p_id = 2
    p, s, d, c = Profile().find_by_pk(2)
    c['hour'] = '*'
    c['minute'] = '*'
    # sched.add_cron_job(Backup.execute, args=[p, s, d], name='wj_%s' % p_id ,**c)
    # sched.add_interval_job(lambda: Backup().execute(s, d), minutes=1)
