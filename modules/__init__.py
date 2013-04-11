import os
from flask import Flask, g
from werkzeug.utils import import_string

""" Load Basic config """
webackup = Flask('modules',
             static_folder="../static",
             template_folder='../templates'
            )

webackup.register_blueprint(import_string('modules.core.controller.register'))