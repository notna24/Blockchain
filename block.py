from cryptography.hazmat.primitives import hashes

import json

from transaction import Transaction

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

	def get_dict(self):
		return {
			"pv_hash": self.pv_hash,
			"transactions": self.transactions,
			"nonce": self.nonce,
			"difficulty": self.difficulty,
			"hash": self.hash
		}

	def get_json(self):
		return json.dumps(self.get_dict())

	def calc_hash(self):
		# miner should not use this function
		pass

	def add_transaction(self, transaction):
		assert isinstance(transaction, Transaction)
		self.transactions.append(transaction)