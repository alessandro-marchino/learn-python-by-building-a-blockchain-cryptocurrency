from time import time
from oop.transaction import Transaction
from oop.printable import Printable

class Block(Printable):
    def __init__(self, index:int, previous_hash:str, transactions:list[Transaction], proof:int, timestamp:float|None=None) -> None:
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time() if timestamp is None else timestamp
        self.transactions=transactions
        self.proof = proof

class JsonableBlock:
    def __init__(self, block:Block):
        self.index = block.index
        self.previous_hash = block.previous_hash
        self.transactions = [ tx.to_ordered_dict() for tx in block.transactions ]
        self.proof = block.proof
        self.timestamp = block.timestamp
