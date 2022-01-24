import blockchain
import mempool
import miner
import wallet
import json




if __name__ == "__main__":
	print("Blockchain started...")

	MP = mempool.MemPool()
	BC = blockchain.Blockchain()
	BC.difficulty = 3

	miner.BLOCKCHAIN = BC
	miner.MEMPOOL = MP

	wallet.BLOCKCHAIN = BC
	wallet.MEMPOOL = MP

	MI = miner.Miner()

	OW = wallet.Wallet() # wallet contains first key with coins on it
	with open("keys/origin_key.json", "r") as key_file:
		json_keys = key_file.read()
	okj = json.loads(json_keys)
	#print(okj.get("public_key"))
	#print(wallet.load_public_pem_key(okj.get("public_key").encode("utf-8")))
	OW.keys.append((okj.get("public_key").encode("utf-8"), okj.get("private_key").encode("utf-8")))
	OW.key_dict[okj.get("public_key").encode("utf-8")] =  okj.get("private_key").encode("utf-8")

	W1 = wallet.Wallet()
	W1.gen_keys()
    
	W2 = wallet.Wallet()
	W2.gen_keys()

	OW.make_auto_transaction([W1.keys[0][0]], [2])
	#print(OW.get_dict())
	bb = BC.blocks
	print(MP.get_dict())
	print(wallet.MEMPOOL.get_dict())
	
	MI.start()
	
	W1.make_auto_transaction(W2.keys[0][0], [1])
	
	