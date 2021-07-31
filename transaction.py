



class Transation:
	def __init__(self, hash=b""):
		self.hash = hash
		self.senders = []
		self.recievers = []
		self.timestamp = 0

	def get_json(self):
		pass