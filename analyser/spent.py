from datetime import datetime
from typing import List, Tuple

from model.Transaction import Transaction


def compute_all_cb_spent(transactions_input: List[Transaction], start_date: datetime, end_date: datetime):
    cb_transactions = filter(lambda transaction: "PAIEMENT CB" in transaction.kind, transactions_input)
    # if print be careful it empties iterator

    cb_transactions_time_filtered = filter(
        lambda trx: start_date < trx.date < end_date, cb_transactions)

    amount_sum = 0
    transaction_count = 0
    for transaction in cb_transactions_time_filtered:
        #  print(transaction)
        amount_sum += transaction.amount
        transaction_count += 1

    return amount_sum
