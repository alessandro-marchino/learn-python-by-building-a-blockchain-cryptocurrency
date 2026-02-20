blockchain = []

def get_last_blockchain_value():
    return blockchain[-1]

def add_value(transaction_amount, last_transaction_value=[1]):
    blockchain.append([last_transaction_value, transaction_amount])

def get_user_input():
    return float(input('Your transaction amount please: '))

add_value(get_user_input())
add_value(last_transaction_value=get_last_blockchain_value(), transaction_amount=get_user_input())
add_value(last_transaction_value=get_last_blockchain_value(), transaction_amount=get_user_input())

print(blockchain)
