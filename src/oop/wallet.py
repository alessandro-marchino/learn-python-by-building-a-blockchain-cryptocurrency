from Crypto.PublicKey import RSA
import Crypto.Random
import binascii

class Wallet:
    def __init__(self) -> None:
        self.private_key = None
        self.public_key = None

    def create_keys(self) -> None:
        private_key, public_key = self.__generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def load_keys(self) -> None:
        pass

    def __generate_keys(self) -> tuple[str, str]:
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (
            binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
            binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
        )
