from functools import reduce
from collections import OrderedDict
from json import dumps, loads

from block import Block

from hash_util import hash_block, hash_string_256

# Initializing our blockchain list
MINING_REWARD = 10
MINING_DIFFICULTY = 2

blockchain = []
open_transactions = []
owner = 'Ale'
participants = { owner }

def load_data():
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as f:
            file_content = f.readlines()
            blockchain = loads(file_content[0][:-1])
            blockchain = [
                Block(
                    block['index'],
                    block['previous_hash'], [
                    OrderedDict([
                        ('sender', tx['sender']),
                        ('recipient', tx['recipient']),
                        ('amount', tx['amount'])
                    ]) for tx in block['transactions']],
                    block['proof'],
                    block['timestamp'])
                for block in blockchain ]

            open_transactions = loads(file_content[1])
            open_transactions = [
                OrderedDict([
                    ('sender', tx['sender']),
                    ('recipient', tx['recipient']),
                    ('amount', tx['amount'])
                    ])
                for tx in open_transactions
            ]
    except (IOError,IndexError):
        genesis_block = Block(0, '', [], -1, 0)
        blockchain = [ genesis_block ]

load_data()

def save_data():
    try:
        with open('blockchain.txt', mode='w') as f:
            f.write(dumps(blockchain))
            f.write('\n')
            f.write(dumps(open_transactions))
    except IOError:
        print('Saving failed!')


def valid_proof(transactions:list, last_hash:str, proof: int) -> bool:
    guess = str(transactions) + str(last_hash) + str(proof)
    guess_hash = hash_string_256(guess)
    return guess_hash[0:MINING_DIFFICULTY] == ('0' * MINING_DIFFICULTY)

def proof_of_work() -> int:
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    nonce = 0
    while not valid_proof(open_transactions, last_hash, nonce):
        nonce += 1
    return nonce

def get_balance(participant:str)-> float:
    tx_sender = [ [ tx['amount'] for tx in block.transactions if tx['sender'] == participant ] for block in blockchain ]
    open_tx_sender = [ tx['amount'] for tx in open_transactions ]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx: tx_sum + sum(tx), tx_sender, 0.0)

    tx_received = [ [ tx['amount'] for tx in block.transactions if tx['recipient'] == participant ] for block in blockchain ]
    amount_received = reduce(lambda tx_sum, tx: tx_sum + sum(tx), tx_received, 0.0)

    return amount_received - amount_sent

def get_last_blockchain_value() -> Block:
    """
    Gets the last block of the blockchain.
    """
    return blockchain[-1]

def verify_transaction(transaction:dict) -> bool:
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

def add_transaction(recipient:str, sender:str=owner, amount:float=1.0) -> bool:
    """
    Append a new value as well as the last transaction value to the blockchain.

    Arguments:
        :sender: The sender of the transaction
        :recepient: The recipient of the transaction
        :amount: The amount sent
    """
    transaction = OrderedDict([
        ('sender', sender),
        ('recipient', recipient),
        ('amount', amount)
    ])
    if not verify_transaction(transaction):
        return False
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)
    save_data()
    return True

def mine_block() -> bool:
    """
    Mines a new blockchain block.
    """
    last_block = blockchain[-1]
    proof = proof_of_work()
    reward_transaction = OrderedDict([
        ('sender', 'MINING'),
        ('recipient', owner),
        ('amount', MINING_REWARD)
    ])

    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hash_block(last_block), copied_transactions, proof)
    blockchain.append(block)
    return True

def get_transaction_value() -> tuple[str, float]:
    """ Returns the input of the user (a transaction recipient and amount) as a tuple. """
    tx_recipient = input('Enter the recipient of the transaction: ')
    user_input = input('Your transaction amount please: ')
    return tx_recipient, float(user_input)

def get_user_choice() -> str:
    """ Returns the user choice. """
    return input('Your choice: ')

def print_blockchain_elements() -> None:
    """ Prints the blockchain elements. """
    for block in blockchain:
        print('Outputting block...')
        print(block)
    else:
        print('-' * 20)

def verify_chain() -> bool:
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print('Proof of work is invalid!')
            return False
    return True

def verify_transactions() -> bool:
    return all([ verify_transaction(tx) for tx in open_transactions ])

waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validity')
    print('q: Exit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Added transaction')
        else:
            print('Transaction failed')
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Choice was invalid, please pick a value from the list!')

    print(f'Balance for {owner}: {get_balance(owner):6.2f}')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        waiting_for_input = False
else:
    print('User left!')

print('Done!')
