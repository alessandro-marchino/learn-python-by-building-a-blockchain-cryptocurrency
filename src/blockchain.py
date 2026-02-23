# Initializing our blockchain list
blockchain = []

def get_last_blockchain_value() -> list:
    """ Returns the last value of the current blockchain. """
    return blockchain[-1]


def add_value(transaction_amount:float, last_transaction_value:list=[1]) -> None:
    """
    Append a new value as well as the last transaction value to the blockchain.

    Arguments:
        :transaction_amount: The amount that should be added
        :last_transaction_value: The last blockchain transaction (default [1])
    """
    blockchain.append([last_transaction_value, transaction_amount])


def get_transaction_value() -> float:
    """ Returns the input of the user (a new transaction amount) as a float. """
    user_input = input('Your transaction amount please: ')
    return float(user_input)

def get_user_choice() -> str:
    return input('Your choice: ')

def print_blockchain_elements() -> None:
    for block in blockchain:
        print('Outputting block...')
        print(block)

add_value(get_transaction_value())

while True:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('q: Exit')
    user_choice = get_user_choice()
    if user_choice == '1':
        add_value(last_transaction_value=get_last_blockchain_value(), transaction_amount=get_transaction_value())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'q':
        pass
    else:
        print('Choice was invalid, please pick a value from the list!')

print('Done!')
