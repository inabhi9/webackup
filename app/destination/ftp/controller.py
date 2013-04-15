from flask import Blueprint, render_template, request
from model import DestinationAct
from lib import resp_format
from base import Error
import form

register = Blueprint('d_ftp', __name__,
                     template_folder='templates')

@register.route('/ftp.html')
def index():
    setting_form = form.SettingForm()
    return render_template('dst_ftp_index.html',
                           form=setting_form,
                           title="File system",
                           test_url='/destination/ftp/testconfig.json')

@register.route('/ftp/testconfig.json', methods=['POST'])
def test_config():
    try:
        DestinationAct(**request.form).test_config()
        msg = 'FTP connection successfully tested'
        return resp_format.from_dict(resp_format.MSG_OK, msg=msg)
    except Error.TestConfigException as e:
        return resp_format.from_dict(resp_format.MSG_FAIL, msg=str(e))
