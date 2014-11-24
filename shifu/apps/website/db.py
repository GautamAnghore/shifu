import pymongo

class ThemeDAO():
	# theme data access object
	def __init__(self,database):
		self.db = database
		self.collection = database.themes

	def add_theme(self,name,author,structures,dirname):

		#theme : name of theme
		#author : name of author of theme
		#structures : list of structures supported by theme
		#dirname : directory name in static/themes/ directory of theme static files

		theme = { '_id':name, 'author':author, 'structures':structures, 'dirname':dirname }

		try:
			self.collection.save(theme, safe=True)
		except pymongo.errors.DuplicateKeyError as e:
			print "pymongo error : duplicate theme name : DuplicateKeyError"
			print e.error_document
			return False
		except pymongo.errors.OperationFailure:
			print "pymongo error : theme could not be saved in db : operation failure"
			return False

		return True

	def get_dir(self,name):

		theme = None

		try:
			theme = self.collection.find_one({'_id':name},{'dirname':True,'_id':False})
		except:
			print "pymongo error : theme search failed : OperationFailure"
			return None

		if theme is not None:
			return theme['dirname']
		else:
			print "pymongo error : theme not found "
			return None

	def get_theme(self,name):

		theme = None

		try:
			theme = self.collection.find_one({'_id':name})
		except:
			print "pymongo error: theme search failed : OperationFailure"
			return None

		if theme is not None:
			return theme
		else:
			print "pymongo error : theme not found"
			return None

	def get_all_theme(self):

		themes = None

		try:
			themes = self.collection.find()
		except:
			print "pymongo error : theme(all) search failed : OperationFailure"
			return None

		if themes is not None:
			return themes
		else:
			print "pymongo error : theme(all) not found"
			return None

	def is_saved(self,dirname):
		#check if theme directory is in db or not
		flag = None

		try:
			if self.collection.find_one({'dirname':dirname}) is not None:
				return True
			else:
				return False
		except:
			return False


