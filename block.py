from cryptography.hazmat.primitives import hashes



## this uses Proof of work method
## but I don*t really like POW method

class Block:
	def __init__(self, header):
		self.header = header
		self.timestamp = 0
		self.transactions = []
		self.nonce = nonce
		self.difficulty = 0


	def get_json(self):
		pass
