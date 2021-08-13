import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils

from blockchain import Blockchain

import json


class Transaction:
	def __init__(self, utxos, inputs=[], outputs=[], ex_addr=None, amounts=[], timestamp=0, fee=0):
		self.inputs = inputs
		self.outputs = outputs
		self.ex_addr = ex_addr if ex_addr != None else self.inputs[len(self.inputs) - 1]
		self.amounts = amounts
		self.timestamp = timestamp
		self.utxos = utxos
		self.fee = fee
		self.hash = b""
		self.siganture = b""

		self.add_ex_addr()

	def add_ex_addr(self):
		utxo_value = 0
		for utxo in self.utxo:
			utxo_value += utxo.amount
		self.outputs.append(self.ex_addr)
		if utxo_value < self.amounts:
			raise("utxo value is smaller than transaction volume")
		self.amounts.append(utxo_value - self.amounts)

	def check_all(self):
		#checks if everything is correct :D
		for input in self.inputs: # maybe change var name "input" to "pub_key"
			if not self.verify(input):
				return False
		for utxo in self.utxos:
			if not Blockchain.check_utxo(utxo):
				return False
		return True
			

	def get_dict(self):
		return {
			"inputs": self.inputs,
			"outputs": self.outputs,
			"amounts": self.amounts,
			"utxos": self.utxos,
			"fee": self.fee,
			"signature": self.signature
		}

	def get_json(self):
		return json.dumps(self.get_dict(), indent=4)

	def calc_hash(self):
		digest = hashes.Hash(hashes.SHA512())
		digest.update(b"hello world")
		return digest.finalize()

	def sign(self, private_key):
		#signs transaction hash
		digest = self.calc_hash()
		self.signature = private_key.sign(
			digest,
			padding.PSS(
				mgf=padding.MGF1(hashes.SHA512()),
				salt_length=padding.PSS.MAX_LENGTH
			),
			#utils.Prehashed(hashes.SHA512()) #nto shure, if I should use prehashed
			hashes.SHA512()
		)

	def verify(self, public_key):
		public_key = self.inputs
		try:
			public_key.verify(
				self.signature,
				self.calc_hash(),
				padding.PSS(
					mgf=padding.MGF1(hashes.SHA512()),
					salt_length=padding.PSS.MAX_LENGTH
				),
				hashes.SHA512()
			)
		except cryptography.exceptions.InvalidSignature:
			return False
		else:
			return True



#utxo = unspend transaction output
#solves double spend problem

class Utxo():
	def __init__(self, transaction_hash, public_key, amount):
		self.transaction_hash = transaction_hash #the hash of the transaction, where the money was send to the adress. Not the adress of the transaction the utxo is used for
		self.pub_key = public_key
		self.amount = amount

	def get_dict(self):
		return {
			"transaction_hash": self.transaction_hash,
			"pub_key": self.pub_key,
			"amount": self.amount
		}

	def get_json(self):
		return json.dumps(self.get_dict())


class CoinbaseTransaction():
	def __init__(self, output, amount):
		self.output = output
		self.amount = amount
		self.hash = self.calc_hash()

	def verify(self):
		return True

	def check_all(self):
		return True

	def get_dict(self):
		return {
			"output": self.output,
			"amount": self.amount,
			"hash": self.hash
		}

	def get_json(self):
		return json.dumps(self.get_dict())

	def calc_hash(self):
		digest = hashes.Hash(hashes.SHA512())
		return digest
		


if __name__ == "__main__":
	t = Transaction(3, [1, 2, 3], [4, 5, 6])
	print(t.get_dict())
	print(t.get_json())
	print(t.calc_hash())
	t.sign()
	print(t.verify())