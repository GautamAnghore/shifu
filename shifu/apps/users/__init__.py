from flask import Blueprint

users = Blueprint('users',__name__,template_folder='templates',static_folder='static',static_url_path='/static/users')
from views import *