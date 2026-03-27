from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
from oop.node import Node

app = Flask(__name__)
CORS(app)
node: Node

@app.route('/', methods=[ 'GET' ])
def get_ui() -> Response:
    return send_from_directory('ui', 'node.html')

@app.route('/network', methods=[ 'GET' ])
def get_network() -> Response:
    return send_from_directory('ui', 'network.html')

@app.route('/wallet', methods=[ 'POST' ])
def create_keys() -> tuple[Response,int]:
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
def load_keys() -> tuple[Response,int]:
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
def get_balance() -> tuple[Response,int]:
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

@app.route('/transaction', methods=[ 'GET' ])
def get_open_transactions() -> tuple[Response,int]:
    open_transactions = node.get_open_transactions()
    dict_transactions = [ tx.to_ordered_dict() for tx in open_transactions ]
    return jsonify(dict_transactions), 200

@app.route('/chain', methods=[ 'GET' ])
def get_chain() -> tuple[Response,int]:
    return jsonify([ block.__dict__ for block in node.get_chain() ]), 200

@app.route('/mine', methods=[ 'POST' ])
def mine() -> tuple[Response,int]:
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
def add_transaction() -> tuple[Response,int]:
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
                'signature': signature
            },
            'funds': node.get_balance()
        }
        return jsonify(response), 201
    response = {
        'message': 'Creating a transaction failed'
    }
    return jsonify(response), 500

@app.route('/node', methods=['POST'])
def add_node() -> tuple[Response,int]:
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data attached'
        }
        return jsonify(response), 400
    if 'node' not in values:
        response = {
            'message': 'No node data found'
        }
        return jsonify(response), 400
    node_value = values['node']
    node.add_node(node_value)
    response = {
        'message': 'Node added successfully',
        'all_nodes': node.get_nodes()
    }
    return jsonify(response), 201

@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url:str) -> tuple[Response,int]:
    if node_url == '' or node_url is None:
        response = {
            'message': 'No node attached'
        }
        return jsonify(response), 400
    node.remove_node(node_url)
    response = {
        'message': 'Node removed successfully',
        'all_nodes': node.get_nodes()
    }
    return jsonify(response), 201

@app.route('/node', methods=['GET'])
def get_nodes() -> tuple[Response,int]:
    response = {
        'all_nodes': node.get_nodes()
    }
    return jsonify(response), 200

# Broadcasts
@app.route('/broadcast/transaction', methods=[ 'POST' ])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = { 'message': 'No data found' }
        return jsonify(response), 400
    required = [ 'sender', 'recipient', 'amount', 'signature' ]
    if not all(key in values for key in required):
        response = { 'message': 'Some data is missing' }
        return jsonify(response), 400
    success = node.add_broadcast_transaction(values['sender'], values['recipient'], values['amount'], values['signature'])
    if success:
        response = {
            'message': 'Successfully added transaction',
            'transaction': {
                'sender': values['sender'],
                'recipient': values['recipient'],
                'amount': values['amount'],
                'signature': values['signature']
            }
        }
        return jsonify(response), 201
    response = {
        'message': 'Broadcasting a transaction failed'
    }
    return jsonify(response), 500

@app.route('/broadcast/block', methods=[ 'POST' ])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = { 'message': 'No data found' }
        return jsonify(response), 400
    if 'block' not in values:
        response = { 'message': 'Some data is missing' }
        return jsonify(response), 400
    node.add_broadcast_block(values['block'])

    try:
        node.add_broadcast_block(values['block'])
        response = { 'message': 'Successfully added block' }
        return jsonify(response), 200
    except ValueError as err:
        response = { 'message': err.args }
        return jsonify(response), 409

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()

    node = Node(args.port)
    app.run(port=args.port)
