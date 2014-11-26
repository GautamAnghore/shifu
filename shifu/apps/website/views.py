from flask import url_for,redirect,render_template,request,session

from apps.website import website
from apps import database
from apps import env

from forms import *
import db

import os
import json

@website.route('/update-enviornment')
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
				obj_theme.add_theme(data['theme-name'],data['author'],data['structures'],subdir)
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
			if obj_structure.issaved(subdir) is False: 
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
	return "done"

@website.route('/refresh-enviornment')
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
				obj_theme.add_theme(data['theme-name'],data['author'],data['structures'],subdir)
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
	return "done"

@website.route('/name',methods=['GET','POST'])
def name():

	obj_website = db.WebsiteDAO(database)

	# for testing session
	#session['first-time']=True

	if request.method == 'GET':
		# no form evaluation
		if 'first-time' in session:
			if session['first-time']==True:
				return render_template('website-name.html',form=WebsiteNameForm())
		
		nameForm = WebsiteNameForm()

		name = obj_website.get_website_name()

		if name is not None:
			nameForm.websitename.data = name

		return render_template('website-name.html',form=nameForm,dashboard=True)

	else:
		# evaluation of form data
		nameForm = WebsiteNameForm(request.form)

		if nameForm.validate():
			#save website name
			obj_website.save_website_name(nameForm.websitename.data)
			return "return to dashboard"
		else:
			#if error and first time visit
			if 'first-time' in session:
				if session['first-time']==True:
					return render_template('website-name.html',form=nameForm)
			#if error but visited from dashboard
			return render_template('website-name.html',form=nameForm,dashboard=True)