
from flask import Flask 
from config import Config
from flask import Blueprint

# application connecting with flask 
app = Flask(__name__)

#configuration
app.config.from_object(Config)

# another way of configuration
#app.config['CSRF_ENABLED'] = True
#app.config['SECRET_KEY'] = 'some_Secret_key_XtksCaSEdc98'

# importing alert module
from alert import *
# importing session handling module
from sessions import *
###################################################################################################################
# source : http://arusahni.net/blog/2014/03/flask-nocache.html
# defination of nocache decorator
from datetime import datetime
from flask import make_response
from functools import update_wrapper

def nocache(f):
    def new_func(*args, **kwargs):
		response = make_response(f(*args, **kwargs))
        #resp.cache_control.no_cache = True
		response.headers['Last-Modified'] = datetime.now()
		response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
		response.headers['Pragma'] = 'no-cache'
		response.headers['Expires'] = '-1'
		return response
    return update_wrapper(new_func, f)
#####################################################################################################################

# database connection
import pymongo

connection = pymongo.MongoClient('localhost',27017)
database = connection.shifu


# blueprint for master of application
master = Blueprint('master',__name__,template_folder='templates',static_folder='static')
from views import *

from users import users
#from users import views
from editor import editor
from dashboard import dashboard
from website import website

#registering all blueprints
app.register_blueprint(master)
app.register_blueprint(users)
app.register_blueprint(editor,url_prefix='/editor')
app.register_blueprint(dashboard,url_prefix='/dashboard')
app.register_blueprint(website,url_prefix='/dashboard/website')
