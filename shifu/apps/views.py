from apps import master
from flask import render_template,url_for,redirect

from apps import database 
import db

# setting the enviornment instance
env = db.Environment(database)

@master.route('/')
def index():
	if env.check_indexset() is False:
		# index page not set
		return redirect( url_for('users.admin') )
	else:
		return render_template('index.html')

@master.route('/',defaults={'path': ''})
@master.route('/<path:path>')
def master_catch(path):
	return "path %s" % path