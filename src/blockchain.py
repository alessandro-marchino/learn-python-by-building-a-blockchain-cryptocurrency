blockchain = []

def get_last_blockchain_value():
    return blockchain[-1]

def add_value(transaction_amount, last_transaction_value=[1]):
    blockchain.append([last_transaction_value, transaction_amount])

tx_amount = float(input('Your transaction amount please: '))
add_value(tx_amount)
tx_amount = float(input('Your transaction amount please: '))
add_value(last_transaction_value=get_last_blockchain_value(), transaction_amount=tx_amount)
tx_amount = float(input('Your transaction amount please: '))
add_value(last_transaction_value=get_last_blockchain_value(), transaction_amount=tx_amount)

print(blockchain)
