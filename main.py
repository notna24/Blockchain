import blockchain
import mempool
import miner
import wallet
import json




if __name__ == "__main__":
	print("Blockchain started...")

	MP = mempool.MemPool()
	BC = blockchain.Blockchain()
	BC.difficulty = 1

	miner.BLOCKCHAIN = BC
	miner.MEMPOOL = MP

	wallet.BLOCKCHAIN = BC
	wallet.MEMPOOL = MP

	MI = miner.Miner()

	OW = wallet.Wallet() # wallet contains first key with coins on it
	with open("keys/origin_key.json", "r") as key_file:
		json_keys = key_file.read()
	okj = json.loads(json_keys)
	OW.keys.append((okj.get("public_key").encode("utf-8"), okj.get("private_key").encode("utf-8")))

	W1 = wallet.Wallet()
	W1.gen_keys()
	
	W2 = wallet.Wallet()
	W2.gen_keys()
	

	OW.make_auto_transaction([W1.keys[0][0]], [2])
	bb = BC.blocks
	
	MI.pub_key = W1.keys[0][0]
	MI.start()
	
	MI.status = False
	
	while len(BC.blocks) == 1:
		continue
	W1.make_auto_transaction([W2.keys[0][0]], [1])
	
	#print("here")
	
	BC.save()
	
	MI.stop()
	MI.join()
	
	print("end")