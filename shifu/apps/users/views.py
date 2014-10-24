from flask import url_for,render_template,redirect, request

from apps.users import users

from forms import *


@users.route('/')
@users.route('/<username>')
def index(username=None):
	if username == None:
		return render_template('silent.html',name='hello world')
	else:
		return render_template('silent.html',name='hello %s' % username)
		#return url_for('users.index')

@users.route('/signup',methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		form = SignupForm(request.form)
		if form.validate():
			return redirect( url_for('.index',username=form.username.data))
		else:
			return render_template('signup.html',form=form,error='validation false')

	return render_template('signup.html',form=SignupForm(),error='first time')
