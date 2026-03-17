from collections import OrderedDict
from utility.printable import Printable
from typing import Literal

class Transaction(Printable):
    def __init__(self, sender:str, recipient:str, amount:float) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_ordered_dict(self) -> OrderedDict[Literal['amount', 'sender', 'recipient'], float | str]:
        return OrderedDict([
            ('sender', self.sender),
            ('recipient', self.recipient),
            ('amount', self.amount)
        ])
