# step : 1 => account_set
# step : 2 => index_page_set
import pymongo
import re

class Environment():

	def __init__(self,database):
		self.database = database
		self.variables = self.database.variables

	def get_variable(self,variable):
		# returns 0 if variable not exists
		flag = None
		
		query = { '_id' : variable}

		try:
			flag = self.variables.find_one(query)
		except:
			return 0

		if flag is not None:
			# variable exists
			print flag['value']
			return flag['value']
		else:
			return 0

	def set_variable(self,variable,value):

		query = { '_id':variable, 'value':value }

		try:
			# save is insert/update, it automatically takes care of update or insert
			self.variables.save(query)
		except pymongo.errors.DuplicateKeyError as e:
			print "DuplicateKeyError: evn set variable %s:%d" % variable,value
			return False
		except pymongo.errors.OperationFailure:
			print "operation failure : evn set variable %s:%d" % variable,value
			return False
		
		return True


	def check_accountset(self):
		# returns True : account is set
		# returns False : account is not set
		
		value = self.get_variable('step')

		if value >= 1:
			return True
		else:
			return False

	def set_accountset(self):

		if self.check_accountset() is False:
			# variable is not already set
			if self.set_variable('step',1) is True:
				return True
			else:
				return False
		else:
			# already set
			return False

	def check_indexset(self):
		# returns True : if index page is set
		# returns False : if not

		value = self.get_variable('step')

		if value >= 2:
			return True
		else:
			return False

	def set_indexset(self):
		 if self.check_indexset() is False:
		 	if self.set_variable('step', 2) is True:
		 		return True
		 	else:
		 		return False
		 else:
		 	return False

	def check_url_restricted(self,url):
		#check if url is in restricted catagory
		#returns true if url is restricted
		#function is kept in this class for future scope of moving restricted list to variables table
		restricted = ['^dashboard','^signin$','^signup$','^signout','^admin','^refresh-enviornment$','^update-enviornment$']

		for pattern in restricted:
			if re.match(pattern,url) is not None:
				return True

		return False
		
