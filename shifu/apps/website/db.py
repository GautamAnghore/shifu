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
	
		try:
			if self.collection.find_one({'dirname':dirname}) is not None:
				return True
			else:
				return False
		except:
			return False

	def drop_themes(self):
		#call with care
		#drop the collection
		self.collection.drop()

class StructureDAO():
	# theme data access object
	def __init__(self,database):
		self.db = database
		self.collection = database.structures

	def add_structure(self,name,author,description,content,dirname):

		#name : name of structure
		#author : name of author of structure
		#description : description about structure
		#content : sub doc containing the content tags with their types
		#dirname : directory name in templates/structures/ directory of structures

		structure = { '_id':name, 'author':author, 'description':description, 'content':content, 'dirname':dirname }

		try:
			self.collection.save(structure, safe=True)
		except pymongo.errors.DuplicateKeyError as e:
			print "pymongo error : duplicate structure name : DuplicateKeyError"
			print e.error_document
			return False
		except pymongo.errors.OperationFailure:
			print "pymongo error : structure could not be saved in db : operation failure"
			return False

		return True

	def get_dir(self,name):

		structure = None

		try:
			structure = self.collection.find_one({'_id':name},{'dirname':True,'_id':False})
		except:
			print "pymongo error : structure search failed : OperationFailure"
			return None

		if structure is not None:
			return structure['dirname']
		else:
			print "pymongo error : structure not found "
			return None

	def get_structure(self,name):

		structure = None

		try:
			structure = self.collection.find_one({'_id':name})
		except:
			print "pymongo error: structure search failed : OperationFailure"
			return None

		if structure is not None:
			return structure
		else:
			print "pymongo error : structure not found"
			return None

	def get_all_structure(self):

		structures = None

		try:
			structures = self.collection.find()
		except:
			print "pymongo error : structure(all) search failed : OperationFailure"
			return None

		if structures is not None:
			return structures
		else:
			print "pymongo error : structure(all) not found"
			return None

	def is_saved(self,dirname):
		#check if structure directory is in db or not
		
		try:
			if self.collection.find_one({'dirname':dirname}) is not None:
				return True
			else:
				return False
		except:
			return False

	def drop_structures(self):
		#call with care
		#drop the collection
		self.collection.drop()

