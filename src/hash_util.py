from hashlib import sha256
from json import dumps
from block import Block

def hash_string_256(string: str) -> str:
    return sha256(string.encode()).hexdigest()

def hash_block(block:Block) -> str:
    """Hashes a block and returns a string representation of it.

    Arguments:
        : block: The block that should be hashed
    """
    hashable_block = block.__dict__.copy()
    return hash_string_256(dumps(hashable_block, sort_keys=True))
