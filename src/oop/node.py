from oop.blockchain import Blockchain
from utility.verification import Verification
from oop.wallet import Wallet

class Node:
    def __init__(self) -> None:
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_transaction_value(self) -> tuple[str, float]:
        """ Returns the input of the user (a transaction recipient and amount) as a tuple. """
        tx_recipient = input('Enter the recipient of the transaction: ')
        user_input = input('Your transaction amount please: ')
        return tx_recipient, float(user_input)

    def get_user_choice(self) -> str:
        """ Returns the user choice. """
        return input('Your choice: ')

    def print_blockchain_elements(self) -> None:
        """ Prints the blockchain elements. """
        for block in self.blockchain.chain:
            print('Outputting block...')
            print(block)
        else:
            print('-' * 20)

    def listen_for_input(self):
        waiting_for_input = True

        while waiting_for_input:
            print('Please choose')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Check transaction validity')
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save wallet')
            print('q: Exit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                assert self.wallet.public_key is not None
                if self.blockchain.add_transaction(recipient, sender=self.wallet.public_key, amount=amount):
                    print('Added transaction')
                else:
                    print('Transaction failed')
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed. Got no wallet?')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain.hosting_node = self.wallet.public_key
                pass
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain.hosting_node = self.wallet.public_key
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Choice was invalid, please pick a value from the list!')

            print(f'Balance for {self.wallet.public_key}: {self.blockchain.get_balance():6.2f}')
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                waiting_for_input = False
        else:
            print('User left!')

        print('Done!')
