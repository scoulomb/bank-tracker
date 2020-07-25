from datetime import datetime
from typing import List

from model.Transaction import Transaction


def find_transaction_gt_abs_ceil(transactions_input: List[Transaction], ceil: float, start_date: datetime,
                                 end_date: datetime):
    transaction_time_filtered = filter(
        lambda trx: start_date < trx.date < end_date, transactions_input)

    return list(filter(lambda transaction: abs(transaction.amount) > ceil, transaction_time_filtered))
