from apps import app

@app.route('/')
@app.route('/<username>')
def index(username=None):
	if username == None:
		return 'hello world'
	else:
		return 'hello %s' % username