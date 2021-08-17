from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from main import MEMPOOL
from transaction import Transaction

import os
import time

class Wallet:
    def __init__(self):
        self.keys= []
        self.balance = 0

    def make_auto_transaction(self):
        return

    def make_transaction(self, inputs, outputs, fee): 
        #for testing purposes it just uses one input
        priv_key, pub_key = gen_key_pair()

        _, pub_key1 = gen_key_pair()

        transaction = Transaction(2)
        transaction.sign(priv_key)
        print(transaction.verify(pub_key))
        print(transaction.verify(pub_key1))

    def store_in_file(self):
        pass

    def load_from_file(self, file_name):
        pass



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


if __name__ == "__main__":
    print(gen_sec_password())