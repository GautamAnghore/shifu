from flask import url_for,render_template,redirect, request, session, make_response

from apps.users import users
from forms import *

import pymongo
import db

from apps import database	# for the database connection
from apps import env	# for enviornment variable operations
from apps import Alert 	# for Alert class 
from apps import nocache # nocache decorator defination
from apps import Sessions 	# session access functions 

user = db.User(database)
alert = Alert()
sessions = Sessions()

@users.route('/admin')
@nocache
def admin():
	# task of admin function is to redirect to appropriate next stage : dashboard or sign in or sign up
	username = sessions.logged_in()
	if username is not None:
		return redirect( url_for('dashboard.dashboard_home',username=username))
	else:
		if env.check_accountset() is True:
			return redirect( url_for('.signin') )
		else:
			return redirect( url_for('.signup') )

@users.route('/signup',methods=['GET','POST'])
def signup():
	if env.check_accountset() is False:
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
					
					sessions.push_username(form.username.data)
					# set its a first time visit
					sessions.push_firsttime()

					return redirect( url_for('website.refresh_enviornment') )
		
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
	else:
		alert.error('Not Authorized')
		return redirect( url_for('.admin') )

@users.route('/signin',methods=['GET','POST'])
@nocache
def signin():
	
	if request.method == 'POST':
		form = SigninForm(request.form)
		
		if form.validate():
			loggedin = user.check_user(form.username.data,form.password.data)

			if loggedin is not None:
				sessions.push_username(form.username.data)
				return redirect( url_for('website.update_enviornment') )
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
		if sessions.logged_in() is not None:
			alert.reset()
			alert.msg('Already Logged In')
			return redirect( url_for('.admin'))
		else:
			if env.check_accountset() is True:
						#testing
						#alert.reset()
						#alert.error('test error')
						#alert.success('some success')
						#alert.msg('some msg')
				resp = make_response(render_template('signin.html',form=SigninForm(),alert=alert.get_alert()))
								
				alert.reset()
				return resp
			else:
				alert.msg('For Logging In, Creating account is Must ')
				return redirect( url_for('.admin'))


@users.route('/signout/<username>',methods=['GET'])
@nocache
def signout(username):
	if sessions.pop_username(username) is True:
		alert.reset()
		alert.success('Logged Out')
		return redirect(url_for('.admin'))
	else:
		alert.reset()
		alert.error('Cannot Log Out ! internal error')
		return redirect(url_for('.admin'))



