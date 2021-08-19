from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from main import MEMPOOL, BLOCKCHAIN
from transaction import Transaction

import os
import time
import json


class Wallet:
    def __init__(self):
        self.keys = [] # will contain key pairs as lists
        self.key_dict = {}

    def list_keys(self):
        for key_pair in self.keys:
            print(key_pair[0])

    def find_standard_fee(self):
        return 0.1

    def make_auto_transaction(self, outputs, amounts):
        amount = 0
        inputs = []
        utxos = []
        for key_pair in self.keys:
            for utxo in BLOCKCHAIN.get_utxos(key_pair[0]):
                amount += utxo.amount
                inputs.append(key_pair[0])
                utxos.append(utxos)
                if amount >= sum(amounts):
                    self.make_transaction(utxos, inputs, outputs, amounts, self.find_standard_fee())
                    return 

    def make_transaction(self, utxos, inputs, outputs, amounts, fee): 
        #needs to find utxo and private keys

        #finding private_keys
        priv_keys = [self.dict[i] for i in self.inputs]

        transaction = Transaction(utxos, inputs, outputs, amounts, fee)

        password = input("please input password: ")

        for pub_key, priv_key in zip(inputs, priv_keys):
            priv_key = load_private_key(priv_key, password)
            transaction.sign(pub_key, priv_key)
        
        password = 0

        r = MEMPOOL.add_transaction(transaction)
        if not r:
            print("transaction could not be added to mempool!")
        else:
            print("transaction made successfully")

    def get_dict(self):
        return {"keys": self.keys}

    def get_json(self):
        return json.dumps(self.get_dict())

    def store_in_file(self, file_name="wallet.json"):
        with open(file_name, "w") as file:
            file.write(self.get_json())

    def load_from_file(self, file_name="wallet.json"):
        with open(file_name, "r") as file:
            content = file.read()
        self.keys = json.loads(content)["keys"]
        for key_pair in self.keys:
            self.key_dict[key_pair[0]] = key_pair[1]



## ALL KEY RELATED STUFF FOLLOWS

def gen_key_pair():
    private_key = gen_private_key()
    return private_key, private_key.public_key()


def gen_serialized_key_pair(password):
    priv_key, pub_key = gen_key_pair()
    return serealize_private_key(priv_key, password), serealize_public_key(pub_key[1])


def gen_private_key():
    return rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )


def gen_sec_password():
    return os.urandom(64)


def serealize_public_key(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem


def serealize_private_key(private_key, password=None):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password) if password != None else serialization.NoEncryption()
    )
    return pem


def load_private_key(pem, password=None):
    return serialization.load_pem_private_key(
        pem,
        password=password
    )


def load_public_pem_key(pem):
    return serialization.load_pem_public_key(
        pem,
        password=None
    )
"""
def laod_key_from_file(file_name="wallet.json"):
    with oepn(file_name, "r") as file:
        content = file.read()
    return json.loads(data)
    """


if __name__ == "__main__":
    print(gen_sec_password())