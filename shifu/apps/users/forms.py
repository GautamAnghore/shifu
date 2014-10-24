from flask_wtf import Form
from wtforms import TextField, PasswordField, validators
from wtforms.validators import Required, Length

class SignupForm(Form):
	username = TextField('Username',validators=[Required('Please provide username'),Length(min=3,message=('Length inappropriate'))])
	password = PasswordField('Password',validators=[Required('password required'),Length(min=5,message=('provide longer password'))])
