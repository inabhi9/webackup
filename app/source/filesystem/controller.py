from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import form
from app.source.filesystem.model import SourceAct
register = Blueprint('s_filesystem', __name__,
                     template_folder='templates')

@register.route('/filesystem.html')
def index():
    setting_form = form.SettingForm()
    return render_template('fs_index.html',
                           form=setting_form,
                           title="File system",
                           test_url = '/source/filesystem/testconfig.json')

@register.route('/filesystem/testconfig.json', methods=['POST'])
def test_config():
    return SourceAct(**request.form).test_config()