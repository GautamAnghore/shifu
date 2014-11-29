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

	def get_all_themes(self):

		cur = None

		try:
			cur = self.collection.find()
		except:
			print "pymongo error : theme(all) search failed : OperationFailure"
			return None

		themes = []
		if cur is not None:
			for doc in cur:
				themes.append(doc['_id'])
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

	def get_applicable_themes(self):
		#get all the themes which contains all the structures definition already in use by pages
		#change the access to pages collection by class object function call rather than directly accessing
		pages = self.db.pages
		try:
			cur = pages.find({},{'structure.name':True,'_id':False})
		except:
			print "cannot find pages, mongodb error"
			return None

		structures = []
		if cur is not None:
			for doc in cur:
				structures.append(doc['structure']['name'])

		#get structures, now search for proper themes
		cur = None
		query = {"structures":{"$all":structures}}

		try:
			cur = self.collection.find(query,{'_id':True})
		except:
			print "cannot find applicable themes, mongodb error"
			return None

		themes = []
		if cur is not None:
			for doc in cur:
				print doc
				themes.append(doc['_id'])
		
		return themes

class StructureDAO():
	# structure data access object
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

	def get_all_structures(self):

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

class WebsiteDAO():
	#variables collection data access object
	#website centered data

	def __init__(self,database):
		self.db = database
		self.collection = database.variables

	def save_website_name(self,name):

		try:
			self.collection.save({'_id':'website-name','value':name})
		except:
			print "pymongo error : website name save error : OperationFailure"
			return False
		return True

	def save_website_theme(self,name):

		try:
			self.collection.save({'_id':'website-theme','value':name})
		except:
			print "pymongo error : website theme save error : OperationFailure"
			return False
		return True

	def get_website_name(self):

		cursor = None
		
		try:
			cursor = self.collection.find_one({'_id':'website-name'})
		except:
			print "pymongo error : website name get error : OperationFailure"
			return None

		if cursor is not None:
			return cursor['value']
		else:
			print "website name not found"
			return None

	def get_website_theme(self):

		cursor = None

		try:
			cursor = self.collection.find_one({'_id':'website-theme'})
		except:
			print "pymongo error : website theme get error : OperationFailure"
			return None

		if cursor is not None:
			return cursor['value']
		else:
			print "website theme not found"
			return None

