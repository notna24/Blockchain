from cryptography.hazmat.primitives import hashes


#from main import BLOCKCHAIN, MEMPOOL
from block import Block, Header


# number of transactions that should be in one block, excluding the coinbase tx
BLOCKSIZE = 2

BLOCKCHAIN = False
MEMPOOL = False

class Miner:
    def __init__(self):
        self.active : bool = True
        self.pub_key = b""

    def mine(self):
        while self.active:
            self.calc_block

    def start(self):
        if self.pub_key == b"":
            print("could not start miner, because no public key was specified!")
            return
        print("started miner")
        self.active = True

    def stop(self):
        print("stoped miner")
        self.active = False


    def get_transactions(self):
        # gets a number of transactions specified by BLOCKSIZE
        if len(MEMPOOL.transactions) < BLOCKSIZE:
            print("Not enough transactions in mempool to form a block!")
            return False
        transactions = MEMPOOL.transactions.sort(key = lambda x: x.fee)
        return transactions[-BLOCKSIZE:]

    def calc_block(self):
        # needs to add coinbase tx to the block xD
        while self.active:
            block = Block()
            block.pv_hash = BLOCKCHAIN.blocks[-1:].calc_hash()
            block.transactions = self.get_transactions
            block.difficulty = BLOCKCHAIN.difficulty
            block_hash = b""
            nonce = 0
            while block_hash[block.difficulty:] != b"0" * block.difficulty and self.active:
                block.nonce = nonce
                block_hash = block.calc_hash()
            print("block found!")
            ret = BLOCKCHAIN.add_block(block)
            if not ret: raise(Exception("block was not valid!"))
            # this part needs to be made more secure
            for tx in block.transactions:
                MEMPOOL.remove(tx)