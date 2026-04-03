from oop.wallet import Wallet
from oop.blockchain import Blockchain
from oop.block import JsonableBlock
from oop.transaction import Transaction
from oop.NetworkError import NetworkError


class Node:
    def __init__(self, node_id: int) -> None:
        self.wallet = Wallet(node_id)
        self.blockchain = Blockchain(self.wallet.public_key, node_id)
        self.node_id = node_id
        pass

    def get_chain(self) -> list[JsonableBlock]:
        chain_snapshot = self.blockchain.chain
        dict_chain = [JsonableBlock(block) for block in chain_snapshot]
        return dict_chain

    def mine(self) -> JsonableBlock | None:
        block = self.blockchain.mine_block()
        return JsonableBlock(block) if block is not None else None

    def create_keys(self) -> bool:
        self.wallet.create_keys()
        if self.wallet.save_keys():
            self.blockchain = Blockchain(self.wallet.public_key, self.node_id)
            return True
        return False

    def load_keys(self) -> bool:
        if self.wallet.load_keys():
            self.blockchain = Blockchain(self.wallet.public_key, self.node_id)
            return True
        return False

    def get_balance(self) -> float | None:
        return self.blockchain.get_balance()

    def add_transaction(self,
                        recipient: str,
                        amount: float) -> tuple[bool, str]:
        if self.wallet.public_key is None:
            return False, ''
        signature = self.wallet.sign_transaction(self.wallet.public_key,
                                                 recipient,
                                                 amount)
        return self.blockchain.add_transaction(self.wallet.public_key,
                                               recipient,
                                               signature,
                                               amount), \
            signature

    def add_broadcast_transaction(self, values: dict):
        if not values:
            raise NetworkError('No data found', 400)
        required = ['sender', 'recipient', 'amount', 'signature']
        if not all(key in values for key in required):
            raise NetworkError('Some data is missing', 400)
        if not self.blockchain.add_transaction(values['sender'],
                                               values['recipient'],
                                               values['signature'],
                                               values['amount'],
                                               True):
            raise NetworkError('Broadcasting a transaction failed', 500)

    def add_broadcast_block(self, values: dict) -> None:
        if not values:
            raise NetworkError('No data found', 400)
        if 'block' not in values:
            raise NetworkError('Some data is missing', 400)
        block = values['block']
        if block['index'] == self.blockchain.chain[-1].index + 1:
            if not self.blockchain.add_block(block):
                raise NetworkError('Block seems invalid', 409)
        elif block['index'] > self.blockchain.chain[-1].index:
            self.blockchain.resolve_conflicts = True
            raise NetworkError(
                'Blockchain seem to differ from local blockchain',
                200)
        else:
            raise NetworkError(
                'Blockchain seem to be shorter, block not added',
                409)

    def get_open_transactions(self) -> list[Transaction]:
        return self.blockchain.get_open_transactions()

    def add_node(self, node) -> None:
        self.blockchain.add_peer_node(node)

    def remove_node(self, node) -> None:
        self.blockchain.remove_peer_node(node)

    def get_nodes(self) -> list[str]:
        return self.blockchain.get_peer_nodes()

    def resolve_conflicts(self) -> bool:
        return self.blockchain.resolve()
