from cryptography.hazmat.primitives import hashes

import threading


#from main import BLOCKCHAIN, MEMPOOL
from block import Block, Header
from transaction import CoinbaseTransaction


# number of transactions that should be in one block, excluding the coinbase tx
BLOCKSIZE = 1

BLOCKCHAIN = False
MEMPOOL = False

class Miner(threading.Thread):
	def __init__(self):
		
		threading.Thread.__init__(self)
		
		self.active : bool = True
		self.pub_key = b""
		
	def run(self):
		self.mine()

	def mine(self):
		self.calc_block()

	def stop(self):
		print("stoped miner")
		self.active = False


	def get_transactions(self):
		# gets a number of transactions specified by BLOCKSIZE
		if len(MEMPOOL.transactions) < BLOCKSIZE:
			return False
		transactions = sorted(MEMPOOL.transactions, key = lambda x: x.fee)
		return transactions[-BLOCKSIZE:]

	def calc_block(self):
		# needs to add coinbase tx to the block xD
		while self.active:
			block = Block()
			block.pv_hash = (BLOCKCHAIN.blocks[-1:][0]).calc_hash()
			if self.get_transactions() == False:
				continue
			block.transactions = self.get_transactions()
			block.add_transaction(CoinbaseTransaction(self.pub_key, 25)) # amount can't be static value

			block.difficulty = BLOCKCHAIN.difficulty
			block_hash = b""
			nonce = 0

			while block_hash[:block.difficulty] != b"\x00" * block.difficulty and self.active:
				block.nonce = nonce
				block_hash = block.calc_hash()
				nonce += 1
				
			ret = BLOCKCHAIN.add_block(block)
			if not ret:
				print("block was not valid!")
				continue
			print("block found!")
			# this part needs to be made more secure
			for tx in block.transactions:
				MEMPOOL.rm_transaction(tx)