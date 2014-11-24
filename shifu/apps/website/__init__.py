from flask import Blueprint

website = Blueprint('website',__name__,static_folder='static',template_folder='templates')

from views import *