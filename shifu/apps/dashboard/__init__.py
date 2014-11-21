from flask import Blueprint

dashboard = Blueprint('dashboard',__name__,static_folder='static',template_folder='templates')

from views import *