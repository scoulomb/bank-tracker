from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    date: datetime
    kind: str
    subKind: str
    label: str
    amount: float


