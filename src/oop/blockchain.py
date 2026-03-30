from oop.block import Block, JsonableBlock
from oop.transaction import Transaction
from oop.wallet import Wallet
from utility.hash_util import hash_block
from utility.verification import Verification

from json import dumps, loads
import requests
from functools import reduce

MINING_REWARD = 10

class Blockchain:
    def __init__(self, public_key:str|None, node_id:int) -> None:
        self.__chain:list[Block] = [ Block(0, '', [], -1, 0) ]
        self.__open_transactions:list[Transaction] = []
        self.__peer_nodes:set[str] = set()
        self.hosting_node = public_key
        self.node_id = node_id
        self.resolve_conflicts = False
        self.load_data()

    @property
    def chain(self) -> list[Block]:
        return self.__chain[:]

    @chain.setter
    def chain(self, val) -> None:
        self.__chain = val

    def get_open_transactions(self) -> list[Transaction]:
        return self.__open_transactions[:]

    def load_data(self) -> None:
        """ Initialize blockchain + import transaction data from file."""
        try:
            with open(f'blockchain-{self.node_id}.txt', mode='r') as f:
                file_content = f.readlines()
                tmp_blockchain = loads(file_content[0][:-1])
                self.chain = [
                    Block(
                        block['index'],
                        block['previous_hash'],
                        [ Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions'] ],
                        block['proof'],
                        block['timestamp'])
                    for block in tmp_blockchain ]

                tmp_transactions = loads(file_content[1][:-1])
                self.__open_transactions = [ Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in tmp_transactions ]

                peer_nodes = loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError,IndexError):
            pass

    def save_data(self) -> None:
        try:
            with open(f'blockchain-{self.node_id}.txt', mode='w') as f:
                saveable_chain = [ jb.__dict__ for jb in [ JsonableBlock(block) for block in self.__chain ] ]
                f.write(dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [ tx.__dict__ for tx in self.__open_transactions ]
                f.write(dumps(saveable_tx))
                f.write('\n')
                f.write(dumps(list(self.__peer_nodes)))
        except IOError:
            print('Saving failed!')

    def proof_of_work(self) -> int:
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        nonce = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, nonce):
            nonce += 1
        return nonce

    def get_balance(self, sender:str|None=None)-> float | None:
        participant = sender if sender is not None else self.hosting_node
        if participant is None:
            return None
        tx_sender = [ [ tx.amount for tx in block.transactions if tx.sender == participant ] for block in self.__chain ]
        open_tx_sender = [ tx.amount for tx in self.__open_transactions if tx.sender == participant ]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx: tx_sum + sum(tx), tx_sender, 0.0)

        tx_received = [ [ tx.amount for tx in block.transactions if tx.recipient == participant ] for block in self.__chain ]
        amount_received = reduce(lambda tx_sum, tx: tx_sum + sum(tx), tx_received, 0.0)

        return amount_received - amount_sent

    def get_last_blockchain_value(self) -> Block:
        """ Gets the last block of the blockchain."""
        return self.__chain[-1]

    def add_transaction(self, sender:str, recipient:str, signature:str, amount=1.0, is_receiving=False) -> bool:
        """
        Append a new value as well as the last transaction value to the blockchain.

        Arguments:
            :sender: The sender of the transaction
            :recepient: The recipient of the transaction
            :amount: The amount sent
        """
        if sender is None:
            return False
        transaction = Transaction(sender, recipient, signature, amount)
        if not Verification.verify_transaction(transaction, self.get_balance):
            return False
        self.__open_transactions.append(transaction)
        if not is_receiving:
            for node in self.__peer_nodes:
                url = f'http://{node}/broadcast/transaction'
                try:
                    response = requests.post(url, json={
                        'sender': sender,
                        'recipient': recipient,
                        'amount': amount,
                        'signature': signature
                    })
                    if response.status_code > 399:
                        print('Transaction declined, needs resolving')
                        return False
                except requests.exceptions.ConnectionError:
                    continue

        self.save_data()
        return True

    def mine_block(self) -> Block | None:
        """
        Mines a new blockchain block.
        """
        if self.hosting_node is None:
            return None

        last_block = self.__chain[-1]
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.hosting_node, '0', MINING_REWARD)

        copied_transactions = self.__open_transactions[:]

        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None

        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hash_block(last_block), copied_transactions, proof)


        self.__chain.append(block)

        self.__open_transactions = []
        self.save_data()
        for node in self.__peer_nodes:
            url = f'http://{node}/broadcast/block'
            try:
                response = requests.post(url, json={ 'block': JsonableBlock(block).__dict__.copy() })
                if response.status_code > 399:
                    print('Block declined, needs resolving')
                    if response.status_code == 409:
                        self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return block

    def add_block(self, block: dict) -> bool:
        transactions = [ Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions'] ]
        proof_is_valid = Verification.valid_proof(transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        self.__chain.append(Block(block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp']))
        stored_transactions = self.__open_transactions[:]
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient'] and opentx.amount == itx['amount'] and opentx.signature == itx['signature']:
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Item wal already removed')

        self.save_data()
        return True

    def add_peer_node(self, node:str) -> None:
        """Adds the new node to the peer node set.

        Arguments:
            :node: the node URL with should be added
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node:str) -> None:
        """Removes the new node from the peer node set.

        Arguments:
            :node: the node URL with should be removed
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self) -> list[str]:
        return sorted(self.__peer_nodes)
