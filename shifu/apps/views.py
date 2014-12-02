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
		url = env.get_indexpage()
		return redirect(url_for('.page_generator',path=url))


@master.route('/<path:path>')
def page_generator(path):

	from apps.pages.db import PagesDAO
	return "path %s" % path