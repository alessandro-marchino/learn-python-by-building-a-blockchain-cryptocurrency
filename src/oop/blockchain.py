from oop.block import Block, JsonableBlock
from oop.transaction import Transaction
from util.hash_util import hash_block
from util.verification import Verification

from json import dumps, loads
from functools import reduce

verifier = Verification()
MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id:str) -> None:
        self.chain: list[Block] = [ Block(0, '', [], -1, 0) ]
        self.open_transactions: list[Transaction] = []
        self.hosting_node = hosting_node_id
        self.load_data()

    def load_data(self) -> None:
        """ Initialize blockchain + import transaction data from file."""
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                tmp_blockchain = loads(file_content[0][:-1])
                self.chain = [
                    Block(
                        block['index'],
                        block['previous_hash'],
                        [ Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions'] ],
                        block['proof'],
                        block['timestamp'])
                    for block in tmp_blockchain ]

                tmp_transactions = loads(file_content[1])
                self.open_transactions = [ Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in tmp_transactions ]
        except (IOError,IndexError):
            pass

    def save_data(self) -> None:
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [ jb.__dict__ for jb in [ JsonableBlock(block) for block in self.chain ] ]
                f.write(dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [ tx.__dict__ for tx in self.open_transactions ]
                f.write(dumps(saveable_tx))
        except IOError:
            print('Saving failed!')

    def proof_of_work(self) -> int:
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        nonce = 0
        while not verifier.valid_proof(self.open_transactions, last_hash, nonce):
            nonce += 1
        return nonce

    def get_balance(self)-> float:
        tx_sender = [ [ tx.amount for tx in block.transactions if tx.sender == self.hosting_node ] for block in self.chain ]
        open_tx_sender = [ tx.amount for tx in self.open_transactions ]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx: tx_sum + sum(tx), tx_sender, 0.0)

        tx_received = [ [ tx.amount for tx in block.transactions if tx.recipient == self.hosting_node ] for block in self.chain ]
        amount_received = reduce(lambda tx_sum, tx: tx_sum + sum(tx), tx_received, 0.0)

        return amount_received - amount_sent

    def get_last_blockchain_value(self) -> Block:
        """ Gets the last block of the blockchain."""
        return self.chain[-1]

    def add_transaction(self, recipient:str, sender:str, amount:float=1.0) -> bool:
        """
        Append a new value as well as the last transaction value to the blockchain.

        Arguments:
            :sender: The sender of the transaction
            :recepient: The recipient of the transaction
            :amount: The amount sent
        """
        transaction = Transaction(sender, recipient, amount)
        if not verifier.verify_transaction(transaction, self.get_balance):
            return False
        self.open_transactions.append(transaction)
        self.save_data()
        return True

    def mine_block(self) -> bool:
        """
        Mines a new blockchain block.
        """
        last_block = self.chain[-1]
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)

        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.chain), hash_block(last_block), copied_transactions, proof)
        self.chain.append(block)

        self.open_transactions = []
        self.save_data()
        return True
