import json


class Blockchain:
    def __init__(self):
        self.blocks = []
        self.difficulty = 0

    
    def add_block(self):
        pass

    def get_json(self):
        pass



class MemPool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        return self.transactions.append((transaction, transaction.hash))

    def rm_transaction(self, transaction):
        if transaction in self.transactions:
            return self.transactions.remvoe(transaction)
        else:
            return False

    def get_json(self):
        pass