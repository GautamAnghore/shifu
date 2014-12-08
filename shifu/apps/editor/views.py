from flask import session,url_for,render_template,redirect,request,make_response

from apps.editor import editor
from apps import database
from apps import Sessions
from apps import env
from apps import nocache,login_required

from forms import *

from apps.pages.db import PagesDAO
from apps.website.db import StructureDAO,ThemeDAO

import bleach
import markdown

sessions = Sessions()

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
@editor.route('/add/<path:path>',methods=['GET','POST'])
@nocache
@login_required
def add_content(path):

	obj_pages = PagesDAO(database)
	obj_structure = StructureDAO(database)

	page = obj_pages.get_page_from_url(path)

	if page is not None:
		
		structure = obj_structure.get_structure(page['structure']['name'])

		#structure for passing in templates
		structure_inputs = structure['content']
		inputs = {}
		for fieldname in structure_inputs:
			inputs[fieldname] = {}
			inputs[fieldname]['type']=structure_inputs[fieldname]
			if structure_inputs[fieldname] == "iterator-markdown" or structure_inputs[fieldname] == "iterator-text":
				inputs[fieldname]['data'] = [""]
				inputs[fieldname]['error'] = []
			else:
				inputs[fieldname]['data'] = ""
				inputs[fieldname]['error'] = ""

		if structure is not None:
			
			if request.method == 'GET':
				return render_template('add-content.html',inputs=inputs,page=page,path=path)

			else:
				# setting bleach settings
				# allowing some tags and attributes
				alw_tags = ['img','span','h1','h2','h3','h4','h5','h6','a','li','ol','ul','abbr','acroynm','b','blockquote','code','em','i','strong','table','tr','td']
				alw_attr = { '*':['class','id'], 'img':['alt','src','style'], 'span':['style'],'a':['href']}

				# content initialised
				content = {}
				#process data
				for fieldname in structure_inputs:
										
					if structure_inputs[fieldname] == "iterator-markdown" or structure_inputs[fieldname] == "iterator-text":
						inputs[fieldname]['data'] = request.form.getlist(fieldname)
						
						content[fieldname] = []

						for md in inputs[fieldname]['data']:
							#bleaching the data
							md = bleach.clean(md,tags=alw_tags,attributes=alw_attr,strip=True)

							if structure_inputs[fieldname] == "iterator-markdown":
								html = markdown.markdown(md)
							else:
								#for simple text we do not want to convert it to html
								html = md

							data = {'html':html,'markdown':md}
							content[fieldname].append(data)

					else:
						inputs[fieldname]['data'] = request.form[fieldname]
						
						md = bleach.clean(inputs[fieldname]['data'],tags=alw_tags,attributes=alw_attr,strip=True)

						if structure_inputs[fieldname] == "simple-markdown":
							html = markdown.markdown(md)
						else:
							#for simple text we do not want to convert it to html
							html = md

						content[fieldname] = {'html':html,'markdown':md}

				if obj_pages.add_page_content(path,content,sessions.logged_in()) is True:
					if env.check_indexset() is False:
						env.set_indexpage(page['_id'])
					return redirect( url_for('users.admin') )
				else:
					return render_template('add-content.html',inputs=inputs,page=page,path=path)

		else:
			print "structure not found"
			return redirect( url_for('users.admin') )

	else:
		print "page not found"
		return redirect( url_for('users.admin') )



@editor.route('/edit/<path:path>',methods=['GET','POST'])
@nocache
@login_required
def edit_content(path):
	
	obj_pages = PagesDAO(database)
	obj_structure = StructureDAO(database)

	page = obj_pages.get_page_from_url(path)

	if page is not None:
		
		structure = obj_structure.get_structure(page['structure']['name'])

		#structure for passing in templates
		structure_inputs = structure['content']
		inputs = {}
		for fieldname in page['structure']['content']:
			inputs[fieldname] = {}
			inputs[fieldname]['type']=structure_inputs[fieldname]
			if (structure_inputs[fieldname] == "iterator-markdown") or (structure_inputs[fieldname] == "iterator-text"):
				inputs[fieldname]['data'] = []
				for item in page['structure']['content'][fieldname]:
					inputs[fieldname]['data'].append(item['markdown'])
			else:
				inputs[fieldname]['data'] = page['structure']['content'][fieldname]['markdown']
				
			

		if structure is not None:
			
			if request.method == 'GET':
				return render_template('edit-content.html',inputs=inputs,page=page,path=path)

			else:
				content = {}
				#process data
				for fieldname in structure_inputs:
										
					if structure_inputs[fieldname] == "iterator-markdown" or structure_inputs[fieldname] == "iterator-text":
						inputs[fieldname]['data'] = request.form.getlist(fieldname)
						
						content[fieldname] = []

						for md in inputs[fieldname]['data']:
							#bleaching the data
							md = bleach.clean(md,strip=True)

							if structure_inputs[fieldname] == "iterator-markdown":
								html = markdown.markdown(md)
							else:
								#for simple text we do not want to convert it to html
								html = md

							data = {'html':html,'markdown':md}
							content[fieldname].append(data)

					else:
						inputs[fieldname]['data'] = request.form[fieldname]
						
						md = bleach.clean(inputs[fieldname]['data'],strip=True)

						if structure_inputs[fieldname] == "simple-markdown":
							html = markdown.markdown(md)
						else:
							#for simple text we do not want to convert it to html
							html = md

						content[fieldname] = {'html':html,'markdown':md}

				if obj_pages.edit_page_content(path,content,sessions.logged_in()) is True:
					return redirect( url_for('users.admin') )
				else:
					return render_template('edit-content.html',inputs=inputs,page=page,path=path)

		else:
			print "structure not found"
			return redirect( url_for('users.admin') )

	else:
		print "page not found"
		return redirect( url_for('users.admin') )