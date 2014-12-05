from flask import url_for,render_template,make_response,request,redirect

from apps.pages import pages
from apps import database
from apps import env
from apps import Sessions

from apps.users import alert

from forms import *
import db
#for structures importing db.py of website blueprint
from apps.website.db import ThemeDAO,WebsiteDAO

sessions = Sessions()

@pages.route('/add',methods=['GET','POST'])
def add():
	obj_theme = ThemeDAO(database)
	structure_list = obj_theme.get_applicable_structures() 
	
	if structure_list is None:
		return redirect( url_for('website.theme'))

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
						return redirect( url_for('editor.add_content',path=form.pageurl.data) )
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
				obj_page.edit_page_meta(path,form.pagename.data,form.pagedesc.data,sessions.logged_in())
				return redirect( url_for('users.admin') )
			else:
				resp = make_response(render_template('edit-page-meta.html',form=form,username=sessions.logged_in(),path=path))
				return resp
		
	else:
		return redirect( url_for('users.admin') )

@pages.route('/edit-url/<path:path>',methods=['GET','POST'])
def edit_url(path):

	obj_page = db.PagesDAO(database)
	page_id = obj_page.get_id_from_url(path)

	if page_id is not None:
		#path is valid
		if request.method == 'GET':
			form = Editpageurl()
			form.pageurl.data = path

			resp = make_response(render_template('change-url.html',form=form,username=sessions.logged_in,path=path))
			return resp

		else:
			#process the data

			form = Editpageurl(request.form)
			
			if form.validate():

				if env.check_url_restricted(form.pageurl.data) is False:
					#check if url belongs to restricted catagory

					if obj_page.check_url_exists(form.pageurl.data) is False:
						#check if url already exists
						#url not exists already, can add url 
						if obj_page.edit_page_url(path,form.pageurl.data,sessions.logged_in()) is True:
							return redirect( url_for('users.admin') )
						else:
							resp = make_response(render_template('change-url.html',form=form,username=sessions.logged_in(),path=path))
							return resp
					else:
						#error : url is already in pages table
						form.pageurl.errors = ['url already exists, please choose a different url']
						resp = make_response(render_template('change-url.html',form=form,username=sessions.logged_in(),path=path))

						return resp
				else:
					# error : url belongs to restricted list
					form.pageurl.errors = ['url is restricted, please choose a different url']
					resp = make_response(render_template('change-url.html',form=form,username=sessions.logged_in(),path=path))

					return resp

			else:
				resp = make_response(render_template('change-url.html',form=form,username=sessions.logged_in(),path=path))

				return resp


	else:
		return redirect( url_for('users.admin') )

@pages.route('/delete',methods=['GET'])
def delete():
	#data access objects
	obj_pages = db.PagesDAO(database)
	obj_website = WebsiteDAO(database)

	#get all the pages with all the details
	pages_cur = obj_pages.get_all_pages()
	
	pages = []

	#converting date modified in displayable format
	if pages_cur is not None:
		for page in pages_cur:
			#source
			#df = datetime.now()
			#df.strftime("%d %B %Y %I:%M%p")
			#result = '28 November 2014 06:31PM'
			
			time = page['datemodified']
			page['datemodified'] = time.strftime("%d %B %Y %I:%M%p")
			pages.append(page)
			

	#get website name
	website_name = obj_website.get_website_name() or "Website"

	resp = make_response(render_template('delete-page.html',username=sessions.logged_in(),alert=alert.get_alert(),website_name=website_name,pages=pages))
	alert.reset()
	return resp

@pages.route('/delete/<path:path>',methods=['GET'])
def delete_page(path):

	obj_pages = db.PagesDAO(database)
	page_id = obj_pages.get_id_from_url(path)
	if page_id is not None:

		if obj_pages.delete_page(page_id) is True:
			alert.success('Page Deleted Successfully')
			return redirect( url_for('.delete') )
		else:
			alert.error('Page Cannot be Deleted')
			return redirect( url_for('.delete') )

	else:
		alert.error('Invalid Access')
		return redirect( url_for('users.admin') )
