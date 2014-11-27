from flask_wtf import Form 
from wtforms import TextField,SelectField,validators
from wtforms.validators import Required,Length

class WebsiteNameForm(Form):

	websitename = TextField('Website Name',validators=[Required('Please Provide the Name'),Length(max=15,message=('please provide a shorter name'))])

class WebsiteThemeForm(Form):

	websitetheme = SelectField('Choose Theme')