from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from peewee import DoesNotExist
from app.core.model import User
register = Blueprint('s_mongodb', __name__,
                     template_folder='templates')
