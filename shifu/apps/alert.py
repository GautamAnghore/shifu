
class Alert():
	def __init__(self):
		self.alert = {}
	def get_alert(self):
		return self.alert
	def reset(self):
		self.alert = {}
	def msg(self,msg=None):
		if msg is None:
			if 'msg' in self.alert:
				return self.alert['msg']
			else:
				return None

		if 'msg' not in self.alert:
			self.alert['msg'] = msg
		else:
			self.alert['msg'] += msg

	def success(self,success):
		if success is None:
			if 'success' in self.alert:
				return self.alert['success']
			else:
				return None
				
		if 'success' not in self.alert:
			self.alert['success'] = success
		else:
			self.alert['success'] += success
	
	def error(self,error):
		if error is None:
			if 'error' in self.alert:
				return self.alert['error']
			else:
				return None
				
		if 'error' not in self.alert:
			self.alert['error'] = error
		else:
			self.alert['error'] += error
	