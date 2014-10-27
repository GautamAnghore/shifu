from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField, validators
from wtforms.validators import Required, Length, EqualTo, Email

class SignupForm(Form):
	
	username = TextField('Username',validators=[Required('Please provide username'),Length(min=3,message=('Length inappropriate'))])
	
	password = PasswordField('Password',validators=[Required('password required'),Length(min=5,message=('Please Provide a longer password')),EqualTo('confirm',message='Passwords Must Match')])
	
	confirm = PasswordField('Confirm Password',validators=[Required('please re-enter the password')])
	
	name = TextField('Full Name',validators=[Required('Please provide your name'),Length(max=30)])
	
	email = TextField('Email',validators=[Email('Email Format do not match')])

class SigninForm(Form):

	username = TextField('Username',validators=[Required('Please provide username'),Length(min=3,message=('Length inappropriate'))])
	
	password = PasswordField('Password',validators=[Required('how can we let you enter without password'),Length(min=5,message=('Please Provide a longer password'))])
	