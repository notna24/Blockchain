from cryptography.hazmat.primitives import hashes

import json

from transaction import Transaction, CoinbaseTransaction

## this uses Proof of work method


# I wanted to use a header with a merkel root, but it's too much effort for me rn. I might add it later.


class Header:
	# not used jet
	def __init__(self, pv_hash : bytes = b"", nonce : int = 0, merkle_root : bytes = b""):
		self.pv_hash = pv_hash
		self.nonce = nonce
		self.merklde_root = merkle_root

	def hash(self):
		pass


	def get_dict(self):
		return {
			"pv_hash": self.pv_hash,
			"nonce": self.nonce,
			"merkle_root": self.merklde_root
		}

	def get_json(self):
		return json.dumps(self.get_dict())

class Block:
	def __init__(self):
		self.header = Header()
		self.timestamp = 0
		self.transactions = []
		self.difficulty = 0
		## should later be in the header
		self.pv_hash = b""
		self.nonce = 0
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
		digest = hashes.Hash(hashes.SHA512())
		composed = self.pv_hash
		for transaction in self.transactions:
			composed += transaction.calc_hash()
		composed += bytes(self.nonce)
		digest.update(composed)
		self.hash = digest.finalize()
		return digest.finalize()

	def add_transaction(self, transaction):
		#assert isinstance(transaction, Transaction)
		self.transactions.append(transaction)

ORIGIN_BLOCK = Block()

with open("keys/origin_key.json", "r") as key_file:
    json_keys = key_file.read()
okj = json.loads(json_keys)

ORIGIN_BLOCK.add_transaction(CoinbaseTransaction(okj.get("public_key").encode("utf-8"), 25))