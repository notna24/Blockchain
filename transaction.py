from cryptography.hazmat.primitives import hashes

from blockchain import MemPool



class Transation:
	def __init__(self, fee=0):
		self.inputs = []
		self.outputs = []
		self.timestamp = 0
		self.fee = fee
		self.hash = b""

	def get_json(self):
		pass

	def calc_hash(self):
		pass


def make_transaction():
	pass

