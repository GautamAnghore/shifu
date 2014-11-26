from flask_wtf import Form 
from wtforms import TextField,validators
from wtforms.validators import Required,Length

class WebsiteNameForm(Form):

	websitename = TextField('Website Name',validators=[Required('Please Provide the Name'),Length(max=15,message=('please provide a shorter name'))])
