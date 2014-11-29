from flask import url_for,render_template,make_response,request,redirect

from apps.pages import pages
from apps import database
from apps import env
from apps import Sessions

from forms import *
import db
#for structures importing db.py of website blueprint
from apps.website.db import StructureDAO

sessions = Sessions()

@pages.route('/add',methods=['GET','POST'])
def add():
	obj_structure = StructureDAO(database)
	structure_cursor = obj_structure.get_all_structures() 
	structure_list = []

	for doc in structure_cursor:
		structure_list.append(doc['_id'])

	if request.method == 'GET':
		
		form = Addpageform()
		form.structurename.choices = [(name,name) for name in structure_list ]

		resp = make_response(render_template('add-page.html',form=form,username=sessions.logged_in()))

		return resp
	else:
		#process the data
		obj_page = db.PagesDAO(database)

		form = Addpageform(request.form)
		form.structurename.choices = [(name,name) for name in structure_list ]

		if form.validate():

			if env.check_url_restricted(form.pageurl.data) is False:
				#check if url belongs to restricted catagory

				if obj_page.check_url_exists(form.pageurl.data) is False:
					#check if url already exists
					#url not exists already, can add url 
					if obj_page.add_page_meta(form.pagename.data,form.pageurl.data,form.structurename.data,form.pagedesc.data,sessions.logged_in()) is True:
						return redirect( url_for('users.admin') )
					else:
						resp = make_response(render_template('add-page.html',form=form,username=sessions.logged_in()))
						return resp
				else:
					#error : url is already in pages table
					form.pageurl.errors = ['url already exists, please choose a different url']
					resp = make_response(render_template('add-page.html',form=form,username=sessions.logged_in()))

					return resp
			else:
				# error : url belongs to restricted list
				form.pageurl.errors = ['url is restricted, please choose a different url']
				resp = make_response(render_template('add-page.html',form=form,username=sessions.logged_in()))

				return resp

		else:
			resp = make_response(render_template('add-page.html',form=form,username=sessions.logged_in()))

			return resp


@pages.route('/edit/<path:path>',methods=['GET','POST'])
def edit_page(path):

	obj_page = db.PagesDAO(database) 
	page_doc = obj_page.get_page_meta(path)

	if page_doc is not None:
		# path is valid
		if request.method == 'GET':
			form = Editpageform()
			form.pagename.data = page_doc['page-name']
			form.pagedesc.data = page_doc['page-description']

			resp = make_response(render_template('edit-page-meta.html',form=form,username=sessions.logged_in(),path=path))
			return resp
		
		else:
			#process the data
			form = Editpageform(request.form)

			if form.validate():
				obj_page.edit_page_meta(path,form.pagename.data,form.pagedesc.data)
				return redirect( url_for('users.admin') )
			else:
				resp = make_response(render_template('edit-page-meta.html',form=form,username=sessions.logged_in(),path=path))
				return resp
		
	else:
		return redirect( url_for('users.admin') )

@pages.route('/edit-url/<path:path>',methods=['GET','POST'])
def edit_url(path):

	obj_page = db.PagesDAO(database)
	return ""
