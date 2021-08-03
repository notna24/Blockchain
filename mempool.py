



class MemPool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        return self.transactions.append((transaction, transaction.hash))

    def rm_transaction(self, transaction):
        if transaction in self.transactions:
            return self.transactions.remove(transaction)
        else:
            return False

    def get_json(self):
        pass