from oop.wallet import Wallet
from oop.blockchain import Blockchain
from oop.block import Block, JsonableBlock
import typing

class Node:
    def __init__(self) -> None:
        self.wallet = Wallet()
        self.blockchain = Blockchain(self.wallet.public_key)
        pass

    def get_chain(self) -> list[dict[str, typing.Any]]:
        chain_snapshot = self.blockchain.chain
        dict_chain = [ JsonableBlock(block).__dict__.copy() for block in chain_snapshot ]
        return dict_chain

    def mine(self) -> JsonableBlock|None:
        block = self.blockchain.mine_block()
        return JsonableBlock(block) if block is not None else None
