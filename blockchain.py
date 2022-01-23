import json

from transaction import Utxo
from block import ORIGIN_BLOCK, Block
from transaction import CoinbaseTransaction

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.difficulty = 0

        self.blocks.append(ORIGIN_BLOCK)

    def check_block(self, block):
        if block.calc_hash()[self.difficulty:] != b"0" * self.difficulty:
            return False

        #check if just one coinbase transaction exists in block
        cb_counter = 0
        #check if all transactinos of the block are valid
        for transaction in block.transactions:
            if not transaction.check_all():
                return False
            if isinstance(transaction, CoinbaseTransaction):
                cb_counter += 1
        if cb_counter != 1:
            return False
        return True
    
    def add_block(self, block):
        assert isinstance(block, Block)
        if self.check_block():
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
                if utxo.transaction_hash == transaction.hash and status != True:
                    for pub_key in transaction.outputs: # changed transaction.inputs to transaction.outputs
                        if utxo.pub_key == pub_key:
                            status = True
        return status
                            
    def get_utxos(self, pub_key):#, amount):
        utxos = []

        for block in self.blocks:
            for transaction in block.transactions:
                for i, output in enumerate(transaction.outputs):
                    print(output)
                    print(pub_key)
                    if output == pub_key:
                        utxo = Utxo(transaction.hash, pub_key, transaction.amounts[i])
                        print("-here-")
                        if self.check_utxo(utxo):
                            utxos.append(utxo)
        return utxos

    def get_dict(self):
        return {
            "blocks": self.blocks
        }

    def get_json(self):
        return json.dumps(self.get_dict())

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
