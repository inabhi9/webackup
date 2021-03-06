from flask import Blueprint, render_template, request
import form
from app.source.filesystem.model import SourceAct
from lib import resp_format
from base import Error

register = Blueprint('s_filesystem', __name__,
                     template_folder='templates')

@register.route('/filesystem.html')
def index():
    setting_form = form.SettingForm()
    return render_template('fs_index.html',
                           form=setting_form,
                           title="File system",
                           test_url='/source/filesystem/testconfig.json')

@register.route('/filesystem/testconfig.json', methods=['POST'])
def test_config():
    try:
        SourceAct(**request.form).test_config()
        msg = 'Directory exists and accessible'
        return resp_format.from_dict(resp_format.MSG_OK, msg=msg)
    except Error.TestConfigException as e:
        return resp_format.from_dict(resp_format.MSG_FAIL, msg=str(e))
