from flask import session,url_for,render_template,redirect,request

from apps.editor import editor
from forms import *

import bleach
import markdown

'''
@editor.route('/')
def edit():
	if 'username' in session:
		return render_template('editor.html',form=EditorForm())
	else:
		return redirect( url_for('users.signin') )

@editor.route('/live',methods=['GET','POST'])
def live():
	if request.method=='POST':
		form = EditorForm(request.form)

		if form.validate():
			if form.content.data != "":
				
				safe_md = bleach.clean(form.content.data,strip=True)

				parsed_html = markdown.markdown(safe_md)

				return render_template('live.html',data=parsed_html)
			else:
				return render_template('live.html',data="lorem ipsum")
		else:
			return render_template('editor.html',form=form,error='invalid validation')

'''
@editor.route('/',methods=['GET','POST'])
def edit_content():
	
	if request.method == 'GET':
		
		return render_template('edit-content.html')

	else:
		header_list = request.form.getlist('header')
		header = []
		for data in header_list:
			header.append(data)
		links_list = request.form.getlist('links')
		links = []
		for data in links_list:
			links.append(data)

		print header
		print links
		return "done"