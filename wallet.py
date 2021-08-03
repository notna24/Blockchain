from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from mempool import Mempool

import os

class Wallet:
    def __init__(self):
        self.keys = []


    def make_transaction(self):
        pass


    def store_in_file(self):
        pass


    def load_from_file(self, file_name):
        pass



## ALL KEY RELATED STUFF FOLLOWS

def gen_key():
    pass


def serealize_public_key(password=None):
    pass


def serealize_private_key(password=None):
    pass