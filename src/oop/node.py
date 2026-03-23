from oop.wallet import Wallet
from oop.blockchain import Blockchain
from oop.block import Block, JsonableBlock

class Node:
    def __init__(self) -> None:
        self.wallet = Wallet()
        self.blockchain = Blockchain(self.wallet.public_key)
        pass

    def get_chain(self):
        chain_snapshot = self.blockchain.chain
        dict_chain = [ JsonableBlock(block).__dict__.copy() for block in chain_snapshot ]
        return dict_chain
