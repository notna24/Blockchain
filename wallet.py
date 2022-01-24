from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

#from main import MEMPOOL, BLOCKCHAIN
from transaction import Transaction

import os
import time
import json


BLOCKCHAIN = False
MEMPOOL = False


class Wallet:
    def __init__(self):
        # self.keys contains private keys in serialized and public key in unserialized form.
        self.keys = [] # will contain key pairs as lists
        self.key_dict = {}
        
    def gen_keys(self, passwd=None):
        priv, pub = gen_serialized_key_pair(passwd)
        self.keys.append((priv, load_public_pem_key(pub)))
        

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
                utxos.append(utxo)
                if amount >= sum(amounts):
                    self.make_transaction(utxos, inputs, outputs, amounts, self.find_standard_fee())
                    return 
        print(amount)
        print(sum(amounts))
        print(len(utxos))
        print("could not make transaction, because your balance was not high enough")

    def make_transaction(self, utxos, inputs, outputs, amounts, fee): 
        #needs to find utxo and private keys

        #finding private_keys
        priv_keys = [self.key_dict[i] for i in inputs]

        transaction = Transaction(utxos=utxos, inputs=inputs, outputs=outputs, amounts=amounts, fee=fee)

		# password must be bytes like
        password = input("please input password: ").encode("utf-8")
        password = password if password != b"" else None

        for pub_key, priv_key in zip(inputs, priv_keys):
            priv_key = load_private_key(priv_key, password)
            transaction.sign(priv_key)
        
        password = 0

        r = MEMPOOL.add_transaction(transaction)
        if r == False:
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
    return serealize_private_key(priv_key, password), serealize_public_key(pub_key)


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


def load_private_key(pem : bytes, password=None):
    return serialization.load_pem_private_key(
        pem,
        password=password
    )


def load_public_pem_key(pem : bytes):
    return serialization.load_pem_public_key(
        pem
        #password=None
    )

def store_key_pair(key_pair, filen="key.json"):
    key_dict = {"private_key" : key_pair[0].decode("utf-8"), "public_key" : key_pair[1].decode("utf-8")}
    json_ob = json.dumps(key_dict)
    with open(filen, "w") as file:
        file.write(json_ob)

"""
def laod_key_from_file(file_name="wallet.json"):
    with oepn(file_name, "r") as file:
        content = file.read()
    return json.loads(data)
    """


if __name__ == "__main__":
    print(gen_sec_password())
    key_pair = gen_serialized_key_pair(None)
    print(str(key_pair[0]))
    print(str(key_pair[1]))
    store_key_pair(key_pair)