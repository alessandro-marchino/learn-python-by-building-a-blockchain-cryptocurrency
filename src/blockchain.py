from functools import reduce
from json import dumps, loads

from oop.block import Block, JsonableBlock
from oop.transaction import Transaction

from util.verification import Verification

from util.hash_util import hash_block

# Initializing our blockchain list
MINING_REWARD = 10

blockchain: list[Block] = []
open_transactions: list[Transaction] = []
owner = 'Ale'
participants = { owner }
verifier = Verification()
