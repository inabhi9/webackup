from flask import Blueprint, render_template, request, redirect, flash
from flask.ext.login import login_user, login_required, logout_user
import form
from peewee import DoesNotExist
from app.core.model import User, UserAuth
from app import SOURCES, DESTINATIONS, login_manager
register = Blueprint('core', __name__,
                     template_folder='templates')


@login_manager.user_loader
def load_user(id):
    usr = User.get(User.id == id)
    return UserAuth(usr.username, usr.id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@register.route('/login', methods=['GET', 'POST'])
def login():
    login_form = form.LoginForm()
    if request.method == 'POST':
        try:
            user = User().authenticate(request.form['field_username'], request.form['field_password'])
            login_user(UserAuth(user.username, user.id))
            return redirect('/')
        except DoesNotExist:
            flash('Invalid username or password', 'error')
        
    return render_template('login.html', form=login_form)

@register.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@register.route('/')
@login_required
def index():
    return render_template('index.html', sources=SOURCES, destinations=DESTINATIONS)

@register.route('/core/list')
@login_required
def lists():
    if request.args.get('type') == 'source':
        return render_template('_source_list.html', sources=SOURCES)
    elif request.args.get('type') == 'destination':
        return render_template('_destination_list.html', sources=DESTINATIONS)

