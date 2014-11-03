# for slow password hashing using pbkdf2_sha256
import pymongo
from passlib.hash import pbkdf2_sha256

class User():

	def __init__(self,database):
		self.db = database
		self.users = database.users

	def secure_password(self,password):
		hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
		return hash

	def add_user(self,username,password,fullName,email=None):
		safe_password = self.secure_password(password)

		user = { '_id':username, 'name':fullName, 'password':safe_password }

		if email is not None:
			user['email'] = email

		try:
			self.users.insert(user, safe=True)
		except pymongo.errors.DuplicateKeyError as e:
			print "duplicate user"
			return False
		except pymongo.errors.OperationFailure:
			print "Operation Failure"
			return False

		return True

	def check_user(self,username,password):

		user = None

		try:
			user = self.users.find_one({'_id':username})
		except:
			return None

		if user is None:
			return None

		if pbkdf2_sha256.verify(password,user['password']):
			return user
		else:
			return None


