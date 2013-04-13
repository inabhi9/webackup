from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from peewee import DoesNotExist
from model import SourceAct
from lib import resp_format
import form

register = Blueprint('d_ftp', __name__,
                     template_folder='templates')

@register.route('/ftp.html')
def index():
    setting_form = form.SettingForm()
    return render_template('dst_ftp_index.html',
                           form=setting_form,
                           title="File system",
                           test_url = '/source/filesystem/testconfig.json')

@register.route('/ftp/testconfig.json', methods=['POST'])
def test_config():
    result = SourceAct(**request.form).test_config()
    return resp_format.from_dict(resp_format.MSG_OK, data={'result' : result})