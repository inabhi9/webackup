import os
from flask import Flask, g
from werkzeug.utils import import_string
from flask_peewee.db import Database

# configure our database
DATABASE = {
    'name': 'data/database.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhhh'

""" Load Basic config """
webackup = Flask('modules',
             static_folder="static",
             template_folder='templates'
            )
webackup.config.from_object(__name__)
webackup.register_blueprint(import_string('app.core.controller.register'))

# instantiate the db wrapper
db = Database(webackup)
