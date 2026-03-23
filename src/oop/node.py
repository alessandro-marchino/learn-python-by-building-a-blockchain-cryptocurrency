from oop.wallet import Wallet
from oop.blockchain import Blockchain
from oop.block import JsonableBlock
import typing

class Node:
    def __init__(self) -> None:
        self.wallet = Wallet()
        self.blockchain = Blockchain(self.wallet.public_key)
        pass

    def get_chain(self) -> list[JsonableBlock]:
        chain_snapshot = self.blockchain.chain
        dict_chain = [ JsonableBlock(block) for block in chain_snapshot ]
        return dict_chain

    def mine(self) -> JsonableBlock|None:
        block = self.blockchain.mine_block()
        return JsonableBlock(block) if block is not None else None

    def create_keys(self) -> bool:
        self.wallet.create_keys()
        if self.wallet.save_keys():
            self.blockchain = Blockchain(self.wallet.public_key)
            return True
        return False

    def load_keys(self) -> bool:
        if self.wallet.load_keys():
            self.blockchain = Blockchain(self.wallet.public_key)
            return True
        return False
