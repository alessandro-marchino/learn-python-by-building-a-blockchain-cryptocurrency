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


def get_user_input() -> float:
    """ Returns the input of the user (a new transaction amount) as a float. """
    return float(input('Your transaction amount please: '))


add_value(get_user_input())
add_value(last_transaction_value=get_last_blockchain_value(), transaction_amount=get_user_input())
add_value(last_transaction_value=get_last_blockchain_value(), transaction_amount=get_user_input())

print(blockchain)
