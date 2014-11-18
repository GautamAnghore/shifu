from flask import Blueprint

editor = Blueprint('editor',__name__,static_folder='static',template_folder='templates')

from views import *