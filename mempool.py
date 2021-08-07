from transaction import Transaction

import json



class MemPool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        assert isinstance(transaction, Transaction)
        if transaction.verify():
            return self.transactions.append(transaction)
        else:
            return False

    def rm_transaction(self, transaction):
        assert isinstance(transaction, Transaction)
        if transaction in self.transactions:
            return self.transactions.remove(transaction)
        else:
            return False

    def get_dict(self):
        return {
                "transactions": self.transactions
        }

    def get_json(self):
        return json.dumps(self.get_dict())

    def save_to_file(self, file_name="mempool.json"):
        with open(file_name, "w") as file:
            file.write(self.get_json())


if __name__ == "__main__":
    mem = MemPool()
    mem.save_to_file()