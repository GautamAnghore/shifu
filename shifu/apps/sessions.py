from flask import session

class Sessions():

	# session handling for users
	def push_username(self,username):
		session['username'] = username

	def logged_in(self,username=None):
		# checks if username passed logged in and return username if logged in
		# if None passed, check session and return the logged in username
		if 'username' in session:
			if session['username'] != "":
				if username is None:
					return session['username']
				else:
					if session['username'] == username:
						return session['username']
					else:
						return None
			else:
				session.pop('username',None)
				return None
		else:
			return None

	def pop_username(self,username):
		if self.logged_in(username) is not None:
			session.pop('username',None)
			return True
		else:
			return False