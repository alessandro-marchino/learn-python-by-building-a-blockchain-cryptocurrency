# Initializing our blockchain list
blockchain = []
open_transactions = []
owner = 'Ale'

def get_last_blockchain_value() -> list[float] | None:
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient: str, sender:str=owner, amount:float=1.0) -> None:
    """
    Append a new value as well as the last transaction value to the blockchain.

    Arguments:
        :sender: The sender of the transaction
        :recepient: The recipient of the transaction
        :amount: The amount sent
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)

def mine_block():
    pass

def get_transaction_value() -> tuple[str, float]:
    """ Returns the input of the user (a new transaction amount) as a float. """
    tx_recipient = input('Enter the recipient of the transaction: ')
    user_input = input('Your transaction amount please: ')
    return tx_recipient, float(user_input)

def get_user_choice() -> str:
    return input('Your choice: ')

def print_blockchain_elements() -> None:
    for block in blockchain:
        print('Outputting block...')
        print(block)
    else:
        print('-' * 20)

def verify_chain():
    for block_index in range(len(blockchain)):
        if block_index > 0 and blockchain[block_index][0] != blockchain[block_index - 1]:
            return False
    return True

waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Exit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'q':
        waiting_for_input = False
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    else:
        print('Choice was invalid, please pick a value from the list!')

    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        waiting_for_input = False
else:
    print('User left!')

print('Done!')
