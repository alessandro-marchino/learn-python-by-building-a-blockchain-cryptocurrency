from time import time
from transaction import Transaction
from collections import OrderedDict

class Block:
    def __init__(self, index: int, previous_hash: str, transactions, proof: int, timestamp:float|None=None) -> None:
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time() if timestamp is None else timestamp
        self.transactions=transactions
        self.proof = proof
