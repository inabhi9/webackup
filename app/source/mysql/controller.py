from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from peewee import DoesNotExist
from app.core.model import User
register = Blueprint('s_mysql', __name__,
                     template_folder='templates')


import form
from model import SourceAct
from lib import resp_format

@register.route('/mysql.html')
def index():
    setting_form = form.SettingForm()
    return render_template('msql_index.html',
                           form=setting_form,
                           title="MySQL",
                           test_url = '/source/mysql/testconfig.json')

@register.route('/mysql/testconfig.json', methods=['POST'])
def test_config():
    result = SourceAct(**request.form).test_config()
    return resp_format.from_dict(resp_format.MSG_OK, data={'result' : result})