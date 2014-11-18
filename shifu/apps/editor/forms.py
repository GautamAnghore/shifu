from flask_wtf import Form 
from wtforms import StringField
from wtforms.widgets import TextArea

class EditorForm(Form):

	content = StringField('WebContent',widget=TextArea())
