from flask import Flask, jsonify, request
from flask_cors import CORS
from oop.node import Node

app = Flask(__name__)
CORS(app)
node: Node

@app.route('/wallet', methods=[ 'POST' ])
def create_keys():
    if node.create_keys():
        response = {
            'public_key': node.wallet.public_key,
            'private_key': node.wallet.private_key,
            'funds': node.get_balance()
        }
        return jsonify(response), 201
    response = {
        'message': 'Saving the keys failed'
    }
    return jsonify(response), 500

@app.route('/wallet', methods=[ 'GET' ])
def load_keys():
    if node.load_keys():
        response = {
            'public_key': node.wallet.public_key,
            'funds': node.get_balance()
        }
        return jsonify(response), 200
    response = {
        'message': 'Loading the keys failed'
    }
    return jsonify(response), 500

@app.route('/balance', methods=[ 'GET' ])
def get_balance():
    balance = node.get_balance()
    if balance is not None:
        response = {
            'message': 'Fetched balance successfully',
            'funds': balance
        }
        return jsonify(response), 200
    response = {
        'message': 'Loading balance failed',
        'wallet_set_up': node.wallet.public_key != None
    }
    return jsonify(response), 500

@app.route('/', methods=[ 'GET' ])
def get_ui() -> str:
    return 'This works'

@app.route('/transaction', methods=[ 'GET' ])
def get_open_transactions():
    open_transactions = node.get_open_transactions()
    dict_transactions = [ tx.to_ordered_dict() for tx in open_transactions ]
    return jsonify(dict_transactions), 200

@app.route('/chain', methods=[ 'GET' ])
def get_chain():
    return jsonify([ block.__dict__ for block in node.get_chain() ]), 200

@app.route('/mine', methods=[ 'POST' ])
def mine():
    block = node.mine()
    if block is not None:
        response = {
            'message': 'Block added successfully',
            'block': block.__dict__,
            'funds': node.get_balance()
        }
        return jsonify(response), 201
    response = {
        'message': 'Adding a block failed',
        'wallet_set_up': node.wallet.public_key != None
    }
    return jsonify(response), 500

@app.route('/transaction', methods=[ 'POST' ])
def add_transaction():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
    required_fields = [ 'recipient', 'amount' ]
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing'
        }
        return jsonify(response), 400
    result, signature = node.add_transaction(values['recipient'], values['amount'])
    if result:
        response = {
            'message': 'Successfully added transaction',
            'transaction': {
                'sender': node.wallet.public_key,
                'recipient': values['recipient'],
                'amount': values['amount'],
                'signature': signature,
                'funds': node.get_balance()
            }
        }
        return jsonify(response), 201
    response = {
        'message': 'Creating a transaction failed'
    }
    return jsonify(response), 500

if __name__ == '__main__':
    node = Node()
    app.run(port=5000)
