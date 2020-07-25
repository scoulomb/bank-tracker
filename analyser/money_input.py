from datetime import datetime
from typing import List, Tuple

from model.Transaction import Transaction


def get_positive_transaction(transactions_input: List[Transaction], start_date: datetime, end_date: datetime) -> List[Transaction]:
    transactions_time_filtered = filter(
        lambda trx: start_date < trx.date < end_date, transactions_input)

    positive_transaction = filter(
        lambda trx: trx.amount > 0, transactions_time_filtered)

    return list(positive_transaction)
