from block import Block
from blockchain import Blockchain
from transaction import Transaction, CoinbaseTransaction, Utxo
from wallet import Wallet
from mempool import MemPool

print("Blockchain started...")

MEMPOOL = MemPool()
BLOCKCHAIN = Blockchain()
