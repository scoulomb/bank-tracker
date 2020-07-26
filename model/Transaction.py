from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    date: datetime
    kind: str
    subKind: str
    label: str
    amount: float

    def __dict__(self):
        """
         We could use asdict dataclass function with dict_factory(transaction_tuple), to transform date and
         and call standard dict, but it would imply replacment in tuble etc so not efficient
         Before dict construction was done in Analyser
        """
        return {"date": self.date.strftime("%Y-%m-%d"),
                "label": self.label,
                "amount": self.amount}
