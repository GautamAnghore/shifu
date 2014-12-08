from flask import url_for,redirect,render_template,request,make_response

from apps.dashboard import dashboard
from apps import nocache,login_required
from apps import database

from apps.users import sessions
from apps.users import alert
from apps.pages.db import PagesDAO
from apps.website.db import WebsiteDAO

@dashboard.route('/<username>')
@nocache
def dashboard_home(username):

	if sessions.logged_in(username) is not None:
		
		#data access objects
		obj_pages = PagesDAO(database)
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

		resp = make_response(render_template('dashboard-home.html',username=username,alert=alert.get_alert(),website_name=website_name,pages=pages))
		alert.reset()
		return resp
	else: 
		#return render_template('errors/401.html',message="invalid user,access denied"),401
		alert.error('Make sure to Log In')
		return redirect( url_for('users.admin') )

@dashboard.route('/help')
@nocache
@login_required
def help():
	return render_template('help.html',username=sessions.logged_in(),alert=alert.get_alert())

@dashboard.route('/about')
@nocache
@login_required
def about():
	return render_template('about.html',username=sessions.logged_in(),alert=alert.get_alert())

@dashboard.route('/markdown')
@nocache
@login_required
def markdown():
	return render_template('markdown.html',username=sessions.logged_in(),alert=alert.get_alert())