import os
from flask import Flask, g
from werkzeug.utils import import_string
from flask_peewee.db import Database
from flask.ext.bootstrap import Bootstrap

# configure our database
DATABASE = {
    'name': 'data/database.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhhh'
CSRF_ENABLED = False

""" Load Basic config """
webackup = Flask('modules',
             static_folder="static",
             template_folder='templates'
            )
webackup.config.from_object(__name__)
Bootstrap(webackup)

# instantiate the db wrapper
db = Database(webackup)

webackup.register_blueprint(import_string('app.core.controller.register'))