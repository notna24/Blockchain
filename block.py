from cryptography.hazmat.primitives import hashes

import json

## this uses Proof of work method
## but I don't really like POW method

class Block:
	def __init__(self, header, nonce, pv_hash):
		self.pv_hash = pv_hash
		self.header = header
		self.timestamp = 0
		self.transactions = []
		self.nonce = nonce
		self.difficulty = 0
		self.hash = b""


	def get_json(self):
		pass


	def get_dic(self):
		pass


	def add_transaction(self, transaction):
		self.transactions.append(transaction, hash)