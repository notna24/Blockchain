from cryptography.hazmat.primitives import hashes

from blockchain import Mempool



class Transation:
	def __init__(self, fee=0):
		self.inputs = []
		self.outputs = []
		self.timestamp = 0
		self.fee = fee
		self.hash = self.calc_hash()

	def get_json(self):
		pass

	def calc_hash(self):
		pass


def make_transaction():
	pass

