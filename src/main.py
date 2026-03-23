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

if __name__ == '__main__':
    node = Node()
    app.run(port=5000)
