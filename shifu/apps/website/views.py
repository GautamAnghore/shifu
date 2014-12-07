from flask import url_for,redirect,render_template,request,session,make_response

from apps.website import website
from apps import database
from apps import env
from apps import Sessions
from apps import nocache,login_required

from apps.users import alert 

from forms import *
import db

import os
import json

sessions = Sessions()

@website.route('/update-enviornment')
@nocache
@login_required
def update_enviornment():

	#update-theme
	#checks new themes and inserts in database
	#checks for new folders only  
	
	obj_theme = db.ThemeDAO(database)

	theme_dir = './apps/static/themes'
	theme_subdir_list = []

	for subdir in os.listdir(theme_dir):
		if os.path.isdir(os.path.join(theme_dir,subdir)):
			if obj_theme.is_saved(subdir) is not True:
				theme_subdir_list.append(subdir)
				#print subdir

	for subdir in theme_subdir_list:
		
		theme = os.path.join(theme_dir,subdir)

		try:
			manifest = open(os.path.join(theme,'manifest.json'))

		except IOError:
			print "themes : manifest.json missing"
			manifest = None
			pass

		if manifest is not None:
			data = json.load(manifest)

			if all( k in data for k in ('theme-name','author','structures')):
				if 'include-files-css' not in data:
					data['include-files-css'] = 'style.css'
				if 'include-files-js' not in data:
					data['include-files-js'] = None

				obj_theme.add_theme(data['theme-name'],data['author'],data['structures'],subdir,data['include-files-css'],data['include-files-js'])
			else:
				print "theme - %s : manifest fault" % subdir

			manifest.close()
		else:
			print "manifest is None"

	#update-structures
	#checks new structures and insert in database
	#checks for new folders only

	obj_structure = db.StructureDAO(database)

	structure_dir = './apps/templates/structures'
	structure_subdir_list = []

	for subdir in os.listdir(structure_dir):
		if os.path.isdir(os.path.join(structure_dir,subdir)) is True:
			if obj_structure.is_saved(subdir) is False: 
				structure_subdir_list.append(subdir)

	for subdir in structure_subdir_list:

		structure = os.path.join(structure_dir,subdir)

		try:
			manifest = open(os.path.join(structure,'manifest.json'))
		except IOError:
			print "structures : manifest.json missing"
			manifest = None
			pass

		if manifest is not None:
			data = json.load(manifest)

			if all( k in data for k in ('structure-name','author','description','content')):
				obj_structure.add_structure(data['structure-name'],data['author'],data['description'],data['content'],subdir)
			else:
				print "structure - %s : manifest fault" % subdir

			manifest.close()
		else:
			print "structures : manifest is None"
	
	#return redirect( url_for('dashboard.themes'))
	return redirect( url_for('users.admin') )

@website.route('/refresh-enviornment')
@nocache
@login_required
def refresh_enviornment():

	#refresh-theme
	#checks new themes as well as old ones for changes and inserts in database
	#checks all the dirs
	
	obj_theme = db.ThemeDAO(database)
	#dropping previous data
	#drop collection of theme
	obj_theme.drop_themes()

	theme_dir = './apps/static/themes'
	theme_subdir_list = []

	for subdir in os.listdir(theme_dir):
		if os.path.isdir(os.path.join(theme_dir,subdir)):
			theme_subdir_list.append(subdir)
			
	for subdir in theme_subdir_list:
		
		theme = os.path.join(theme_dir,subdir)

		try:
			manifest = open(os.path.join(theme,'manifest.json'))

		except IOError:
			print "manifest.json missing"
			manifest = None
			pass

		if manifest is not None:
			data = json.load(manifest)

			if all( k in data for k in ('theme-name','author','structures')):
				if 'include-files-css' not in data:
					data['include-files-css'] = 'style.css'
				if 'include-files-js' not in data:
					data['include-files-js'] = None

				obj_theme.add_theme(data['theme-name'],data['author'],data['structures'],subdir,data['include-files-css'],data['include-files-js'])
			else:
				print "theme - %s : manifest fault" % subdir
				
			manifest.close()
		else:
			print "manifest is None"
	
	#refresh-structures
	#checks new and old structures and insert and update data in database
	#checks for new as well as old folders 

	obj_structure = db.StructureDAO(database)
	#drop structures
	#drop collection
	obj_structure.drop_structures()

	structure_dir = './apps/templates/structures'
	structure_subdir_list = []

	for subdir in os.listdir(structure_dir):
		if os.path.isdir(os.path.join(structure_dir,subdir)) is True:
			structure_subdir_list.append(subdir)

	for subdir in structure_subdir_list:

		structure = os.path.join(structure_dir,subdir)

		try:
			manifest = open(os.path.join(structure,'manifest.json'))
		except IOError:
			print "structures : manifest.json missing"
			manifest = None
			pass

		if manifest is not None:
			data = json.load(manifest)

			if all( k in data for k in ('structure-name','author','description','content')):
				obj_structure.add_structure(data['structure-name'],data['author'],data['description'],data['content'],subdir)
			else:
				print "structure - %s : manifest fault" % subdir

			manifest.close()
		else:
			print "structures : manifest is None"
	
	#return redirect( url_for('dashboard.themes'))
	if sessions.is_firsttime() is True:
		return redirect( url_for('.name') )
	else:
		alert.reset()
		alert.success('Enviornmet Updated Successfully')
		return redirect( url_for('users.admin') )

@website.route('/name',methods=['GET','POST'])
@nocache
@login_required
def name():

	obj_website = db.WebsiteDAO(database)

	# for testing session
	#session['first-time']=True

	if request.method == 'GET':
		# no form evaluation
		if sessions.is_firsttime() is True:
			alert.reset()
			alert.msg('Set a name for your website')
			resp = make_response(render_template('new-website-name.html',form=WebsiteNameForm(),username=sessions.logged_in(),alert=alert.get_alert()))
			alert.reset()
			return resp
	
		nameForm = WebsiteNameForm()

		name = obj_website.get_website_name()

		if name is not None:
			nameForm.websitename.data = name

		return render_template('change-website-name.html',form=nameForm,username=sessions.logged_in())

	else:
		# evaluation of form data
		nameForm = WebsiteNameForm(request.form)

		if nameForm.validate():
			#save website name
			obj_website.save_website_name(nameForm.websitename.data)
			if sessions.is_firsttime() is True:
				alert.success('Website Name Saved')
				return redirect( url_for('.theme') )
			else:
				alert.success('Successfully changed website name')
				return redirect( url_for('users.admin') )
		else:
			#if error and first time visit
			if sessions.is_firsttime() is True:
				alert.reset()
				alert.error('Please Provide Appropriate Name')
				resp = make_response(render_template('new-website-name.html',form=nameForm,username=sessions.logged_in(),alert=alert.get_alert()))
				alert.reset()
				return resp
			#if error but visited from dashboard
			alert.reset()
			alert.error('Not a valid name to change')
			resp = make_response(render_template('change-website-name.html',form=nameForm,username=sessions.logged_in(),alert=alert.get_alert()))
			alert.reset()
			return resp

@website.route('/theme',methods=['GET','POST'])
@nocache
@login_required
def theme():

	obj_website = db.WebsiteDAO(database)
	obj_theme = db.ThemeDAO(database)
	themes = []
	#for development testing
	#sessions.push_firsttime()
	if sessions.is_firsttime() is True:
		# will show all the themes
		themes = obj_theme.get_all_themes()
	else:
		# we only wish to show those themes which have all the used structures
		# get a list of all the structures being used
		themes = obj_theme.get_applicable_themes()
	
	if request.method == 'GET':
		form = WebsiteThemeForm()
		form.websitetheme.choices = [(name,name) for name in themes]

		if sessions.is_firsttime() is True:
			alert.msg('Choose a theme for your website')
			resp = make_response(render_template('new-website-theme.html',themes=themes,form=form,alert=alert.get_alert()))
			alert.reset()
			return resp
		
		else:
			chosen_data = obj_website.get_website_theme()
			form.websitetheme.data = chosen_data
			return render_template('change-website-theme.html',themes=themes,form=form,username=sessions.logged_in())
	else:
		#process data
		themeForm = WebsiteThemeForm(request.form)
		themeForm.websitetheme.choices = [(name,name) for name in themes]

		if themeForm.validate():

			obj_website.save_website_theme(themeForm.websitetheme.data)

			if sessions.is_firsttime() is True:
				sessions.pop_firsttime()
				alert.success('Website Theme Saved')
				return redirect( url_for('users.admin') )
			
			alert.success('Theme Changed')			
			return redirect( url_for('users.admin') )
		
		else:
			if sessions.is_firsttime() is True:
				alert.reset()
				alert.error('Not appropriate Theme')
				resp = make_response(render_template('new-website-theme.html',themes=themes,form=themeForm,alert=alert.get_alert()))
				alert.reset()
				return resp
			else:
				alert.reset()
				alert.error('Cannot Change Theme, Input is not valid')
				resp = make_response(render_template('change-website-theme.html',themes=themes,form=themeForm,username=sessions.logged_in(),alert=alert.get_alert()))
				alert.reset()
				return resp


