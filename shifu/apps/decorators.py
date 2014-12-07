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

from flask import redirect,url_for

from alert import *
alert = Alert()

from sessions import *
sessions = Sessions()

def login_required(f):
	def new_func(*args, **kwargs):
		if sessions.logged_in() is not None:

			return f(*args, **kwargs)

		else:
			alert.error('Invalid Access')
			return redirect( url_for('users.admin') )

	return update_wrapper(new_func,f)
