from flask import Flask, jsonify
from flask_cors import CORS
from oop.node import Node

app = Flask(__name__)
CORS(app)
node: Node

@app.route('/', methods=[ 'GET' ])
def get_ui() -> str:
    return 'This works'

@app.route('/chain', methods=[ 'GET' ])
def get_chain():
    return jsonify(node.get_chain()), 200

@app.route('/mine', methods=[ 'POST' ])
def mine():
    block = node.mine()
    if block is not None:
        response = {
            'message': 'Block added successfully',
            'block': block
        }
        return jsonify(response), 201
    response = {
        'message': 'Adding a block failed',
        'wallet_set_up': node.wallet.public_key != None
    }
    return jsonify(response), 500

if __name__ == '__main__':
    node = Node()
    app.run(port=5000)
