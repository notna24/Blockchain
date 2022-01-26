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

	#def start(self):
	#	if self.pub_key == b"":
	#		print("could not start miner, because no public key was specified!")
	#		return
	#	print("started miner")
	#	self.active = True

	def stop(self):
		print("stoped miner")
		self.active = False


	def get_transactions(self):
		# gets a number of transactions specified by BLOCKSIZE
		if len(MEMPOOL.transactions) < BLOCKSIZE:
			#print("Not enough transactions in mempool to form a block!")
			return False
		transactions = sorted(MEMPOOL.transactions, key = lambda x: x.fee)
		#print(transactions)
		return transactions[-BLOCKSIZE:]

	def calc_block(self):
		# needs to add coinbase tx to the block xD
		while self.active:
			#print(MEMPOOL.transactions)
			block = Block()
			#print(BLOCKCHAIN.blocks[len(BLOCKCHAIN.blocks) - 1])
			block.pv_hash = (BLOCKCHAIN.blocks[-1:][0]).calc_hash()
			#print(self.get_transactions())
			if self.get_transactions() == False:
				continue
			block.transactions = self.get_transactions()
			block.add_transaction(CoinbaseTransaction(self.pub_key, 25)) # amount can't be static value

			block.difficulty = BLOCKCHAIN.difficulty
			block_hash = b""
			nonce = 0
			print(block.transactions)
			while block_hash[:block.difficulty] != b"\x00" * block.difficulty and self.active:
				#print(block_hash[block.difficulty:], b"\x00" * block.difficulty)
				#if block_hash[block.difficulty:] == b"\x00":
				#	print("found block dd")
				#print(block_hash[:block.difficulty])
				block.nonce = nonce
				block_hash = block.calc_hash()
				#print(block.transactions)
				#print(block_hash[0])
				nonce += 1
			print("block found!")
			ret = BLOCKCHAIN.add_block(block)
			if not ret: raise(Exception("block was not valid!"))
			# this part needs to be made more secure
			for tx in block.transactions:
				MEMPOOL.rm_transaction(tx)