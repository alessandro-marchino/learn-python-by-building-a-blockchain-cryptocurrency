from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii

from oop.transaction import Transaction

class Wallet:
    def __init__(self) -> None:
        self.private_key = None
        self.public_key = None

    def create_keys(self) -> None:
        private_key, public_key = self.__generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self) -> None:
        if self.public_key is not None and self.private_key is not None:
            try:
                with open('wallet.txt', mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
            except (IOError, IndexError):
                print('Saving wallet failed')

    def load_keys(self) -> None:
        try:
            with open('wallet.txt', mode='r') as f:
                keys = f.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
        except (IOError, IndexError):
            print('Loading wallet failed')

    def __generate_keys(self) -> tuple[str, str]:
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (
            binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
            binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
        )

    def sign_transaction(self, sender:str, recipient:str, amount:float) -> str:
        if self.private_key is None:
            return ''

        signer = PKCS1_v1_5.new(RSA.import_key(binascii.unhexlify(self.private_key)))
        payload = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(payload)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(tx:Transaction) -> bool:
        if tx.sender == 'MINING':
            return True
        pub = RSA.import_key(binascii.unhexlify(tx.sender))
        verifier = PKCS1_v1_5.new(pub)
        payload = SHA256.new((str(tx.sender) + str(tx.recipient) + str(tx.amount)).encode('utf8'))
        return verifier.verify(payload, binascii.unhexlify(tx.signature))
