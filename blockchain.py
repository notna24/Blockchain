import json

from transaction import Utxo
from block import ORIGIN_BLOCK, Block
from transaction import CoinbaseTransaction

class Blockchain:
	def __init__(self):
		self.blocks = []
		self.difficulty = 1

		self.blocks.append(ORIGIN_BLOCK)

	def check_block(self, block):
		if block.calc_hash()[:self.difficulty] != b"\x00" * self.difficulty:
			return False

		#check if just one coinbase transaction exists in block
		cb_counter = 0
		#check if all transactinos of the block are valid
		print(block.transactions)
		for transaction in block.transactions:
			if not transaction.check_all(self):
				return False
			print(transaction)
			if isinstance(transaction, CoinbaseTransaction):
				cb_counter += 1
		if cb_counter != 1:
			return False
		return True
	
	def add_block(self, block):
		assert isinstance(block, Block)
		if self.check_block(block):
			self.blocks.append(block)
			return True
		return False

	def check_utxo(self, utxo):
		status = False
		for block in self.blocks:
			for transaction in block.transactions:
				for transaction_utxo in transaction.utxos:
					# checks if utxo is already spend
					if utxo.transaction_hash == transaction_utxo.transaction_hash:
						return False
				#print(utxo.transaction_hash, transaction.calc_hash())
				if utxo.transaction_hash == transaction.calc_hash() and status != True:
					for pub_key in transaction.outputs: # changed transaction.inputs to transaction.outputs
						if utxo.pub_key == pub_key:
							status = True
		return status
							
	def get_utxos(self, pub_key):#, amount):
		utxos = []

		for block in self.blocks:
			for transaction in block.transactions:
				for i, output in enumerate(transaction.outputs):
					if output == pub_key:
						utxo = Utxo(transaction.calc_hash(), pub_key, transaction.amounts[i])
						if self.check_utxo(utxo):
							utxos.append(utxo)
		return utxos

	def get_dict_d(self):
		return {
			"blocks": self.blocks
		}
	
	def get_dict(self):
		return {f'block_{i}': b.get_dict() for i, b in enumerate(self.blocks) }
	
	def get_str_dict(self):
		print("\n", {f'block_{i}': b.get_str_dict() for i, b in enumerate(self.blocks) })
		return {f'block_{i}': b.get_str_dict() for i, b in enumerate(self.blocks) }

	def get_json(self):
		return json.dumps(self.get_str_dict())

	def save(self, name="blockchain.json"):
		with open(name, "w") as file:
			file.write(self.get_json())

	def load_from_json(self, name="blockchain.json"):
		with open(name, "r") as file:
			json_chain = json.load(file)
		self.blocks = json_chain["blocks"]


if __name__ == "__main__":
	chain = Blockchain()
	chain.blocks = [1, 2, 3]
	chain.save()

	chain2 = Blockchain()
	chain2.load_from_json()
	print(chain2.blocks)
