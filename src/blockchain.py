from functools import reduce
from json import dumps, loads

from oop.block import Block, JsonableBlock
from oop.transaction import Transaction

from util.verification import Verification

from util.hash_util import hash_block

# Initializing our blockchain list
MINING_REWARD = 10

blockchain: list[Block] = []
open_transactions: list[Transaction] = []
owner = 'Ale'
participants = { owner }
verifier = Verification()

def load_data():
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as f:
            file_content = f.readlines()
            tmp_blockchain = loads(file_content[0][:-1])
            blockchain = [
                Block(
                    block['index'],
                    block['previous_hash'],
                    [ Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions'] ],
                    block['proof'],
                    block['timestamp'])
                for block in tmp_blockchain ]

            tmp_transactions = loads(file_content[1])
            open_transactions = [ Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in tmp_transactions ]
    except (IOError,IndexError):
        genesis_block = Block(0, '', [], -1, 0)
        blockchain = [ genesis_block ]

load_data()

def save_data():
    try:
        with open('blockchain.txt', mode='w') as f:
            saveable_chain = [ jb.__dict__ for jb in [ JsonableBlock(block) for block in blockchain ] ]
            f.write(dumps(saveable_chain))
            f.write('\n')
            saveable_tx = [ tx.__dict__ for tx in open_transactions ]
            f.write(dumps(saveable_tx))
    except IOError:
        print('Saving failed!')

def proof_of_work() -> int:
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    nonce = 0
    while not verifier.valid_proof(open_transactions, last_hash, nonce):
        nonce += 1
    return nonce

def get_balance(participant:str)-> float:
    tx_sender = [ [ tx.amount for tx in block.transactions if tx.sender == participant ] for block in blockchain ]
    open_tx_sender = [ tx.amount for tx in open_transactions ]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx: tx_sum + sum(tx), tx_sender, 0.0)

    tx_received = [ [ tx.amount for tx in block.transactions if tx.recipient == participant ] for block in blockchain ]
    amount_received = reduce(lambda tx_sum, tx: tx_sum + sum(tx), tx_received, 0.0)

    return amount_received - amount_sent

def get_last_blockchain_value() -> Block:
    """
    Gets the last block of the blockchain.
    """
    return blockchain[-1]

def add_transaction(recipient:str, sender:str=owner, amount:float=1.0) -> bool:
    """
    Append a new value as well as the last transaction value to the blockchain.

    Arguments:
        :sender: The sender of the transaction
        :recepient: The recipient of the transaction
        :amount: The amount sent
    """
    transaction = Transaction(sender, recipient, amount)
    if not verifier.verify_transaction(transaction, get_balance):
        return False
    open_transactions.append(transaction)
    save_data()
    return True

def mine_block() -> bool:
    """
    Mines a new blockchain block.
    """
    last_block = blockchain[-1]
    proof = proof_of_work()
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)

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
        if verifier.verify_transactions(open_transactions, get_balance):
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Choice was invalid, please pick a value from the list!')

    print(f'Balance for {owner}: {get_balance(owner):6.2f}')
    if not verifier.verify_chain(blockchain):
        print_blockchain_elements()
        print('Invalid blockchain!')
        waiting_for_input = False
else:
    print('User left!')

print('Done!')
