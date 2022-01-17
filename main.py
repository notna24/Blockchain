import blockchain
import mempool
import miner
import wallet




if __name__ == "__main__":
    print("Blockchain started...")

    MP = mempool.MemPool()
    BC = blockchain.Blockchain()

    miner.BLOCKCHAIN = BC
    miner.MEMPOOL = MP

    wallet.BLOCKCHAIN = BC
    miner.MEMPOOL = MP

    MI = miner.Miner()
    W1 = wallet.Wallet()
    W2 = wallet.Wallet()
