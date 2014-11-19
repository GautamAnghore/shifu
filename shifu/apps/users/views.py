from flask import url_for,render_template,redirect, request, session, make_response

from apps.users import users
from forms import *

import pymongo
import db

from apps import database	# for the database connection
from apps import env	# for enviornment variable operations
from apps import Alert 	# for Alert class 
from apps import nocache # nocache decorator defination

user = db.User(database)
alert = Alert()


@users.route('/admin')
@nocache
def admin():
	# task of admin function is to redirect to appropriate next stage : dashboard or sign in or sign up
	username = logged_in()
	if username is not None:
		return redirect( url_for('.dashboard',username=username))
	else:
		if env.check_accountset() is True:
			return redirect( url_for('.signin') )
		else:
			return redirect( url_for('.signup') )


@users.route('/dashboard/<username>')
@nocache
def dashboard(username):

	if logged_in(username) is not None:
		alert.success('Logged In')
		resp = make_response(render_template('temp_dashboard.html',username=username,alert=alert.get_alert()))

		alert.reset()
		return resp
	else: 
		#return render_template('errors/401.html',message="invalid user,access denied"),401
		alert.error('Make sure to Log In')
		return redirect( url_for('.admin') )

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
				env.set_accountset()
				
				session_push_username(form.username.data)
				return redirect( url_for('.admin'))
			else:
				alert.reset()
				alert.error('cannot add user, internal error')
				return render_template('signup.html',form=form,alert=alert.get_alert())
		

		else:
			alert.reset()
			alert.error('Please Provide appropriate input')
			return render_template('signup.html',form=form,alert=alert.get_alert())

	if alert.msg() is None:
		alert.msg('Admin Account Setup')
	return render_template('signup.html',form=SignupForm(),alert=alert.get_alert())


@users.route('/signin',methods=['GET','POST'])
@nocache
def signin():
	
	if request.method == 'POST':
		form = SigninForm(request.form)
		
		if form.validate():
			loggedin = user.check_user(form.username.data,form.password.data)

			if loggedin is not None:
				session_push_username(form.username.data)
				return redirect( url_for('.admin') )
			else:
				alert.reset()
				alert.error('Wrong Credentials')
				return render_template('signin.html',form=form,alert=alert.get_alert() )

		else:
			alert.reset()
			alert.error('Please Provide Appropriate Details')
			return render_template('signin.html',form=form,alert=alert.get_alert())
	else:
		#return render_template('silent.html',form=SigninForm(),error='first time')
		if logged_in() is not None:
			alert.reset()
			alert.msg('Already Logged In')
			return redirect( url_for('.admin'))
		else:
			if env.check_accountset() is True:

				resp = make_response(render_template('signin.html',form=SigninForm(),alert=alert.get_alert()))
								
				alert.reset()
				return resp
			else:
				alert.msg('For Logging In, Creating account is Must ')
				return redirect( url_for('.admin'))


@users.route('/signout/<username>',methods=['GET'])
@nocache
def signout(username):
	if session_pop_username(username) is True:
		alert.reset()
		alert.success('Logged Out')
		return redirect(url_for('.admin'))
	else:
		alert.reset()
		alert.error('Cannot Log Out ! internal error')
		return redirect(url_for('.admin'))


# session handling for users
def session_push_username(username):
	session['username'] = username

def logged_in(username=None):
	# checks if username passed logged in and return username if logged in
	# if None passed, check session and return the logged in username
	if 'username' in session:
		if session['username'] != "":
			if username is None:
				return session['username']
			else:
				if session['username'] == username:
					return session['username']
				else:
					return None
		else:
			session.pop('username',None)
			return None
	else:
		return None

def session_pop_username(username):
	if logged_in(username) is not None:
		session.pop('username',None)
		return True
	else:
		return False
