from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from mempool import MemPool

import os

class Wallet:
    def __init__(self):
        self.keys= []


    def make_transaction(self):
        pass


    def store_in_file(self):
        pass


    def load_from_file(self, file_name):
        pass



## ALL KEY RELATED STUFF FOLLOWS

def gen_key_pair():
    private_key = gen_private_key()
    return (private_key, private_key.public_key())


def gen_private_key():
    return rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )



def serealize_public_key(public_key, password=None):
    public_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def serealize_private_key(private_key, password=None):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCSB,
        encryption_algorithm=serialization.BestAvailableEncryption(password) if password != None else serialization.NoEncryption()
    )