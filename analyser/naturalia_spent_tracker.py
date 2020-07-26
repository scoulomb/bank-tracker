from datetime import datetime
from typing import List, Tuple

from model.Transaction import Transaction


def analyse_naturalia_spent(transactions_input: List[Transaction], start_date: datetime, end_date: datetime):
    naturalia_transactions = filter(lambda transaction: "NATURALIA" in transaction.label, transactions_input)
    # if print be careful it empties iterator

    naturalia_transactions_time_filtered = filter(
        lambda trx: start_date < trx.date < end_date, naturalia_transactions)
    #print(len(list((naturalia_transactions_time_filtered))))
    amount_sum = 0
    transaction_count = 0
    for transaction in naturalia_transactions_time_filtered:
        amount_sum += transaction.amount
        transaction_count += 1


    delta = (end_date - start_date).days
    sum_per_day = amount_sum / delta
    avg_basket = amount_sum / transaction_count

    return amount_sum, sum_per_day, avg_basket
