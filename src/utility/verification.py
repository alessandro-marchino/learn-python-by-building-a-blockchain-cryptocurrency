""" Provides verification helper methods. """
from oop.block import Block
from oop.transaction import Transaction
from oop.wallet import Wallet

from utility.hash_util import hash_block, hash_string_256
from collections.abc import Callable

MINING_DIFFICULTY = 2

class Verification:
    @staticmethod
    def valid_proof(transactions:list[Transaction], last_hash:str, proof:int) -> bool:
        guess = str([ tx.to_ordered_dict() for tx in transactions ]) + str(last_hash) + str(proof)
        guess_hash = hash_string_256(guess)
        return guess_hash[0:MINING_DIFFICULTY] == ('0' * MINING_DIFFICULTY)


    @classmethod
    def verify_chain(cls, blockchain:list[Block]) -> bool:
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid!')
                return False
        return True


    @staticmethod
    def verify_transaction(transaction:Transaction, get_balance:Callable[...,float|None], check_funds=True) -> bool:
        if check_funds:
            sender_balance = get_balance(transaction.sender)
            if sender_balance is None:
                return False
            print(sender_balance, transaction.amount)
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions:list[Transaction], get_balance:Callable[...,float]) -> bool:
        return all([ cls.verify_transaction(tx, get_balance, False) for tx in open_transactions ])
