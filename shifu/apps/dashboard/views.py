from flask import url_for,redirect,render_template,request

from apps.dashboard import dashboard

import os
import json

@dashboard.route('/theme/list')
def themes():
	theme_dir = './apps/static/themes/'
	theme_list = []
	response = ""

	for item in os.listdir(theme_dir):
		if os.path.isdir(os.path.join(theme_dir,item)):
			theme_list.append(item)

	for item in theme_list:
		theme = os.path.join(theme_dir,item)	# path of theme directory
		try:
			manifest = open(os.path.join(theme,'manifest.json'))
			data = json.load(manifest)
			if 'theme-name' in data:
				response += "Theme name : %s" % data['theme-name']
			if 'author' in data:
				response += "author : %s" % data['author']
			manifest.close()
		except IOError:
			pass

	return "%s" % response
