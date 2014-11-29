from flask_wtf import Form
from wtforms import TextField,SelectField,TextAreaField,validators
from wtforms.validators import Required,Length,Regexp

class Addpageform(Form):

	pagename = TextField('Page Name',
				validators=[Required('Please give your page a name'),
							Regexp('^[\w \d \s]+$',
							message=('Use of Invalid Characters')),
							Length(max=30,message=('Please Provide shorter name'))
							],
				description='Unique name for page e.g. Home, Index...'
						)

	pageurl = TextField('Page Url',
				validators=[Regexp('^[^/]\S+[/\S]+$',
							message=('Format of url do not qualify the criteria')),
							Required('Please provide a url'),
							Length(max=100,message=('Please Provide a shorter path'))],
				description='Subpath for page e.g. home, example/example, xyz/xyz/xyz'
					)

	structurename = SelectField('Structure',
				validators=[Required('Please Select any structure for your page')],
				description='Choose a structure for the page')

	pagedesc = TextAreaField('Page Description',
				validators=[Required('Please provide a short description for your page'),
							Regexp('^[\w \s \d @ # $ % . , / ? *]+$',
							message=('Use of Invalid Characters')),
							Length(max=200,message=('Please Provide a shorter page Description'))],
				description='A short description for the page'
						)

class Editpageform(Form):

	pagename = TextField('Page Name',
				validators=[Required('Please give your page a name'),
							Length(max=30,message=('Please Provide shorter name')),
							Regexp('^[\w \d \s]+$',
							message=('Use of Invalid Characters'))
							],
				description='Unique name for page e.g. Home, Index...'
						)
	pagedesc = TextAreaField('Page Description',
				validators=[Required('Please provide a short description for your page'),
							Regexp('^[\w \s \d @ # $ % . , / ? *]+$',
							message=('Use of Invalid Characters')),
							Length(max=200,message=('Please Provide a shorter page Description'))],
				description='A short description for the page'
						)

class Editpageurl(Form):

	pageurl = TextField('Page Url',
				validators=[Regexp('^[^/]\S+[/\S]+$',
							message=('Format of url do not qualify the criteria')),
							Required('Please provide a url'),
							Length(max=100,message=('Please Provide a shorter path'))],
				description='Subpath for page e.g. home, example/example, xyz/xyz/xyz'
					)