import os
from flask import Flask, g
from werkzeug.utils import import_string
from flask_peewee.db import Database
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.shelve_store import ShelveJobStore

# configure our database
DATABASE = {
    'name': 'data/database.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhhh'
CSRF_ENABLED = False
APP_DIR = 'app'
BOOTSTRAP_JQUERY_VERSION = None
SOURCES = []; DESTINATIONS = []


""" Load Basic config """
webackup = Flask('modules',
             static_folder="static",
             template_folder='templates'
            )
webackup.config.from_object(__name__)
Bootstrap(webackup)

# instantiate the db wrapper
db = Database(webackup)

# instatiate the login
login_manager = LoginManager()
login_manager.setup_app(webackup)

# initiate scheduler
sched = Scheduler()
sched.add_jobstore(ShelveJobStore('data/scheduler.db'), 'default')
sched.start()

""" Registering the blueprint controller """
dirs = os.listdir(APP_DIR)
for module in dirs:
    """ Blueprints """
    try:
        if module.startswith('__'): continue
        webackup.register_blueprint(import_string(APP_DIR + '.' + module + '.controller.register'))
    except ImportError, e:
        pass


dirs = os.listdir(APP_DIR + '/source')
for module in dirs:
    """ Blueprints """
    try:
        if module.startswith('__'): continue
        webackup.register_blueprint(import_string(APP_DIR + '.source.' + module + '.controller.register'), url_prefix='/source')
    except ImportError, e:
        pass
    
    """ Populate supported sources"""
    try:
        t = import_string(APP_DIR + '.source.' + module + '.info')
        SOURCES.append(t)
    except ImportError, e:
        pass
    
dirs = os.listdir(APP_DIR + '/destination')
for module in dirs:
    """ Blueprints """
    try:
        if module.startswith('__'): continue
        webackup.register_blueprint(import_string(APP_DIR + '.destination.' + module + '.controller.register'), url_prefix='/destination')
    except ImportError, e:
        pass
        
    """ Populate supported destinations """
    try:
        t = import_string(APP_DIR + '.destination.' + module + '.info')
        DESTINATIONS.append(t)
    except ImportError, e:
        pass
