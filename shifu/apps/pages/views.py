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
			if obj_page.add_page_meta(form.pagename.data,form.pageurl.data,form.structurename.data,form.pagedesc.data,sessions.logged_in()) is True:
				return redirect( url_for('users.admin') )
			else:
				resp = make_response(render_template('add-page.html',form=form,username=sessions.logged_in()))
				return resp
		else:
			resp = make_response(render_template('add-page.html',form=form,username=sessions.logged_in()))

			return resp


@pages.route('/edit/',defaults={'path': ''})
@pages.route('/edit/<path:path>')
def edit_page(path):
	return "path : %s" % path
