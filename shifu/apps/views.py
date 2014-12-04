from apps import master
from flask import render_template,url_for,redirect

from apps import database

import db

# setting the enviornment instance
env = db.Environment(database)


@master.route('/')
def index():
	if env.check_indexset() is False:
		# index page not set
		return redirect( url_for('users.admin') )
	else:
		url = env.get_indexpage()
		return redirect(url_for('.page_generator',path=url))


@master.route('/<path:path>')
def page_generator(path):

	from apps.pages.db import PagesDAO
	from apps.website.db import StructureDAO
	from apps.website.db import ThemeDAO
	from apps.website.db import WebsiteDAO

	#importing required db class
	#importing locally as globally is causing an error in importing env in pages
	
	obj_pages = PagesDAO(database)
	obj_structure = StructureDAO(database)
	obj_theme = ThemeDAO(database)
	obj_website = WebsiteDAO(database)

	if obj_pages.check_url_exists(path):

		#get page's all the information
		page = obj_pages.get_page_from_url(path)

		#the structure page is using
		structure_name = page['structure']['name']
		
		#getting structure dict
		structure = obj_structure.get_structure(structure_name)

		#formatting data variable for the output
		data = {}
		for fieldname in page['structure']['content']:

			if structure['content'][fieldname] == "iterator-markdown" or structure['content'][fieldname] == "iterator-text":
				data[fieldname] = []
				for list_item in page['structure']['content'][fieldname]:
					data[fieldname].append(list_item['html'])
			else:
				data[fieldname] = page['structure']['content'][fieldname]['html']

		#getting structure path
		structure_path = "structures/" + structure['dirname'] +"/structure.html"

		#getting theme name
		theme_name = obj_website.get_website_theme()

		#getting theme
		theme = obj_theme.get_theme(theme_name)

		#theme directory
		theme_path = "themes/" + theme['dirname'] +"/"

		data['includes'] = {}
		data['includes']['css'] = []
		data['includes']['js'] = []

		import os
		#structure specific theme
		structure_specific_theme = url_for('static',filename=theme_path + structure['_id'] +".css")

		if os.path.isfile("./apps" + structure_specific_theme):
			print "yes css"
			data['includes']['css'].append(structure_specific_theme)

		#structure specific js
		structure_specific_js = url_for('static',filename=theme_path + structure['_id'] +".js")

		if os.path.isfile("./apps" + structure_specific_js):
			print "yes js"
			data['includes']['js'].append(structure_specific_js)

		for item in theme['include-files-css']:
			data['includes']['css'].append(url_for('static',filename=theme_path+item))

		for item in theme['include-files-js']:
			data['includes']['js'].append(url_for('static',filename=theme_path+item))
		
		data['title'] = obj_website.get_website_name() + page['page-name']

		return render_template(structure_path,data=data)


	else:

		return "error 404 page not found %s" % path