from flask import Flask
from flask_cors import CORS
from oop.wallet import Wallet

app = Flask(__name__)
CORS(app)
wallet = Wallet()

@app.route('/', methods=[ 'GET' ])
def get_ui() -> str:
    return 'This works'

if __name__ == '__main__':
    app.run(port=5000)


# from oop.node import Node

# if __name__ == '__main__':
#     node = Node()
#     node.listen_for_input()
