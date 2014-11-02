from flask import url_for,render_template,redirect, request, session

from apps.users import users
from forms import *

import pymongo
import db

from apps import database	# for the database connection

user = db.User(database)

@users.route('/admin')
@users.route('/admin/<username>')
def admin(username=None):
	if username == None:
		return render_template('admin.html',form=SigninForm())
	else:
		if 'username' in session:
			if session['username'] == username:
				new_user = {}
				new_user['username']=username
				return render_template('admin.html',user=new_user)
			else:
				return render_template('errors/401.html',message="invalid user,access denied"),401
		else:
			return render_template('errors/401.html',message="invalid user,access is denied"),401

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
				session['username']=form.username.data
				return redirect( url_for('.admin',username=form.username.data))
			else:
				return render_template('signup.html',form=form,error='cannot add user,internal error')
		

		else:
			return render_template('signup.html',form=form,error='validation false')

	return render_template('signup.html',form=SignupForm(),error='first time')


@users.route('/signin',methods=['GET','POST'])
def signin():
	if request.method == 'POST':
		form = SigninForm(request.form)
		
		if form.validate():
			loggedin = user.check_user(form.username.data,form.password.data)

			if loggedin is not None:
				session['username']=form.username.data
				return redirect( url_for('.admin',username=form.username.data) )
			else:
				return render_template('admin.html',form=form,error='wrong credentials' )

		else:
			return render_template('admin.html',form=form)

	#return render_template('silent.html',form=SigninForm(),error='first time')
	return redirect( url_for('.admin'))

@users.route('/signout',methods=['GET'])
def signout():
	session.pop('username',None)
	return redirect(url_for('.admin'))