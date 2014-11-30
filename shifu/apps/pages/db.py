import pymongo
from datetime import datetime

#df = datetime.now()
#df.strftime("%d %B %Y %I:%M%p")
#result = '28 November 2014 06:31PM'

# not using url as _id as need to update it

class PagesDAO():

	def __init__(self,database):
		self.db = database
		self.collection = database.pages

	def add_page_meta(self,pagename,url,structurename,pagedesc,createdby):
		#adds metadata for page
		#content is added via editor
		#url should start from character like abc/somepath and not /abc/somepath

		datemodified = datetime.now()
		# as initially modified by the same person as created by
		modifiedby = createdby

		structure = { 'name':structurename }
		new_page = { 'url':url, 'page-name':pagename, 'page-description':pagedesc, 'structure':structure, 'createdby':createdby, 'modifiedby':modifiedby, 'datamodified':datemodified}

		try:
			self.collection.insert(new_page, safe=True)
		except pymongo.errors.DuplicateKeyError as e:
			print "pymongo error : add page failure : Duplicate Key"
			return False
		except pymongo.errors.OperationFailure:
			print "pymongo error : add page failure : OperationFailure"
			return False

		return True

	def check_url_exists(self,url):
		#use this while creating new page or updating url

		doc = None
		
		try:
			doc = self.collection.find_one({'url':url})
		except:
			print "pymongo error : searching for url : OperationFailure"
			return True # return true because this function is intended to be used 
						#to check if url exists while creating new page
						# we do not want to let a new page be created with duplicate url
						# in case of operational failure

		if doc is not None:
			return True #url exists
		else:
			return False #url not exists

	def get_page_from_url(self,url):
		#use this for serving the page request
		#returns page present on passed url
		#no page results none

		doc = None

		try:
			doc = self.collection.find_one({'url':url})
		except:
			print "pymongo error : searching page error : OperationFailure"
			return None

		if doc is not None:
			return doc
		else:
			return None

	def get_id_from_url(self,url):
		#used by edit_page_url method
		#use this for updating the url
		#returns id of the page corrosponding to passed url
		#no page results none

		doc = None

		try:
			doc = self.collection.find_one({'url':url},{'_id':True})
		except:
			print "pymongo error : searching page error : OperationFailure"
			return None

		if doc is not None:
			return doc['_id']
		else:
			return None

	def edit_page_url(self,old_url,new_url,modifiedby):
		#edit the url of page
		page_id = self.get_id_from_url(old_url)

		if page_id is not None:
			try:
				self.collection.update({'_id':page_id},{'$set':{'url':new_url,'modifiedby':modifiedby}})
			except:
				print "pymongo error : cannot update the url"
				return False
			return True
		else:
			return False

	def get_page_meta(self,url):

		doc = None

		try:
			doc = self.collection.find_one({'url':url},{'_id':False,'page-name':True,'page-description':True})
		except:
			print "pymongo error : searching page error [get page meta] : OperationFailure"
			return None

		if doc is not None:
			return doc
		else:
			return None

	def edit_page_meta(self,url,pagename,pagedesc,modifiedby):
		#edit the pagename and pagedescription

		page_id = self.get_id_from_url(url)

		if page_id is not None:
			try:
				self.collection.update({'_id':page_id},{'$set':{'page-name':pagename,'page-description':pagedesc,'modifiedby':modifiedby}})
			except:
				print "pymongo error : cannot update page meta"
				return False

			return True
		else:
			return False

	def add_page_content(self,url,content,modifiedby):

		page_id = self.get_id_from_url(url)
		
		if page_id is not None:
			try:
				self.collection.update({'_id':page_id},{'$set':{'structure.content':content}})
			except:
				print "pymongo error: cannot update with content"
				return False

			return True
		else:
			return False




		
