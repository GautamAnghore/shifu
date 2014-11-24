from flask import url_for,redirect,render_template,request

from apps.website import website
from apps import database

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
	#return redirect( url_for('dashboard.themes'))
	return "done"

@website.route('/refresh-enviornment')
def refresh_enviornment():

	#refresh-theme
	#checks new themes as well as old ones for changes and inserts in database
	#checks all the dirs
	
	obj_theme = db.ThemeDAO(database)

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
	#return redirect( url_for('dashboard.themes'))
	return "done"
								