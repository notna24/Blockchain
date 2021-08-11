import json

from transaction import Utxo
from block import Block


class Blockchain:
    def __init__(self):
        self.blocks = []
        self.difficulty = 0
    
    def add_block(self, block):
        assert isinstance(block, Block)
        pass

    def check_utxo(self, utxo):
        status = False
        for block in self.blocks:
            for transaction in block.transactions:
                for transaction_utxo in transaction.utxos:
                    # checks if utxo is already spend
                    if utxo.transaction_hash == transaction_utxo.transaction_hash:
                        status = False
                        break
                if utxo.transaction_hash == transaction.hash and status != True:
                    for pub_key in transaction.inputs:
                        if utxo.pub_key == pub_key:
                            status = True
        return status
                            
    def get_utxos(self, pub_key, amount):
        utxos = []

        for block in self.blocks:
            for transaction in self.transactions:
                for i, output in enumerate(transaction.outputs):
                    if output == pub_key:
                        utxo = Utxo(transaction.hash, pub_key, transaction.amounts[i])
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
