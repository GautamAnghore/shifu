from flask import url_for,render_template,redirect, request

from apps.users import users
from forms import *

import pymongo
import db

connection = pymongo.MongoClient('localhost',27017)
database = connection.shifu

user = db.User(database)

@users.route('/')
@users.route('/<username>')
def index(username=None):
	if username == None:
		return redirect( url_for('.signin') )
	else:
		return render_template('silent.html',username='hello %s' % username)
		#return url_for('users.index')

@users.route('/signup',methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		
		form = SignupForm(request.form)
		
		if form.validate():
			# form validation success
			# can add to db
			if form.email.data != "":
				success = user.add_user(form.username.data,form.password.data,form.name.data,form.email.data)
			else:
				success = user.add_user(form.username.data,form.password.data,form.name.data)

			
			if success is True:
				return redirect( url_for('.index',username=form.username.data))
			else:
				return redirect( url_for('./signup/error'),error='cannot add user')
		

		else:
			return render_template('signup.html',form=form,error='validation false')

	return render_template('signup.html',form=SignupForm(),error='first time')

@users.route('/signup/error',methods=['GET','POST'])
def signup_error(error):
	return error

@users.route('/signin',methods=['GET','POST'])
def signin():
	if request.method == 'POST':
		form = SigninForm(request.form)

		if form.validate():
			loggedin = user.check_user(form.username.data,form.password.data)

			if loggedin is not None:
				return redirect( url_for('.index',username=form.username.data) )
			else:
				return render_template('silent.html',form=form,error='wrong credentials' )

		else:
			return render_template('silent.html',form=form)

	return render_template('silent.html',form=SigninForm(),error='first time')