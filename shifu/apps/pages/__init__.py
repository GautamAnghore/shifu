from flask import Blueprint

pages = Blueprint('pages',__name__,static_folder='static',template_folder='templates')

from views import *