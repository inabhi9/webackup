from flask import Blueprint, render_template

register = Blueprint('core', __name__,
                     template_folder='templates')


@register.route('/')
def index():
    return render_template('index.html')

@register.route('/login')
def login():
    return render_template('login.html')