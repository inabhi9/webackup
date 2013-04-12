from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import form
from peewee import DoesNotExist
from app.core.model import User
from app import SOURCES, DESTINATIONS
register = Blueprint('core', __name__,
                     template_folder='templates')


@register.route('/')
def index():
    return render_template('index.html', sources=SOURCES, destinations=DESTINATIONS)

@register.route('/login', methods=['GET', 'POST'])
def login():
    login_form = form.LoginForm()
    if request.method == 'POST':
        try:
            user = User().authenticate(request.form['field_username'], request.form['field_password'])
            session['logged_in'] = True
            session['id'] = user.id
            session['username'] = user.username
            return redirect('/')
        except DoesNotExist:
            flash('Invalid username or password', 'error')
        
        #flash('You were logged in')
        
    return render_template('login.html', form=login_form)

@register.route('/logout')
def logout():
    try:
        session.pop('logged_in')
        session.pop('id')
        session.pop('username')
    except:
        return redirect('/login')
    
    return redirect('/login')