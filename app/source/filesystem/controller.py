from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from peewee import DoesNotExist
import form
register = Blueprint('s_filesystem', __name__,
                     template_folder='templates')

@register.route('/filesystem')
def index():
    setting_form = form.SettingForm()
    return render_template('fs_index.html', form=setting_form, title="File system")