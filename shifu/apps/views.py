from apps import master
from flask import render_template,url_for

@master.route('/')
def index():
	return render_template('index.html')