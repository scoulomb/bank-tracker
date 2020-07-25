from datetime import datetime
from typing import List, Tuple

from model.Transaction import Transaction


def find_max_negative_transaction_using_cb(transactions_input: List[Transaction], start_date: datetime, end_date: datetime):
    cb_transactions = filter(lambda transaction: "PAIEMENT CB" in transaction.kind, transactions_input)
    # if print be careful it empties iterator

    transaction_time_filtered = filter(
        lambda trx: start_date < trx.date < end_date, cb_transactions)
    return min(transaction_time_filtered, key=lambda trx: trx.amount)
