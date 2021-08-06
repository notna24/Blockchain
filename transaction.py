import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils

import json


class Transaction:
	def __init__(self, utxo, inputs=[], outputs=[], timestamp=0, fee=0):
		self.inputs = inputs
		self.outputs = outputs
		self.timestamp = timestamp
		self.utxo = utxo
		self.fee = fee
		self.hash = b""

		self.siganture = b""

	def get_dict(self):
		return {
			"inputs": self.inputs,
			"outputs": self.outputs,
			"timestamp": self.timestamp,
			"fee": self.fee,
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


class Coinbase():
	def __init__(self, output, amount):
		self.output = output
		self.amount = amount

	def verify(self):
		return True


if __name__ == "__main__":
	t = Transaction(3, [1, 2, 3], [4, 5, 6])
	print(t.get_dict())
	print(t.get_json())
	print(t.calc_hash())
	t.sign()
	print(t.verify())