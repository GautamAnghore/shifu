
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

#importing decorators
from decorators import *

# database connection
import pymongo

connection = pymongo.MongoClient('localhost',27017)
database = connection.shifu


# blueprint for master of application
master = Blueprint('master',__name__,template_folder='templates',static_folder='static')
from views import *

from users import users
from editor import editor
from dashboard import dashboard
from website import website
from pages import pages

#registering all blueprints
app.register_blueprint(master)
app.register_blueprint(users)
app.register_blueprint(dashboard,url_prefix='/dashboard')
app.register_blueprint(website,url_prefix='/dashboard/website')
app.register_blueprint(pages,url_prefix='/dashboard/page')
app.register_blueprint(editor,url_prefix='/dashboard/page/content')


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404
