from datetime import datetime
from typing import List

from model.Transaction import Transaction


class Analyser:
    def __init__(self, transactions_input: List[Transaction]):
        self.transactions_input = transactions_input
        self.transactions_input_context = transactions_input

    def reset(self):
        self.transactions_input_context = self.transactions_input

    def get_transactions(self) -> List[Transaction]:
        return self.transactions_input_context

    def filter_date(self, start_date: datetime, end_date: datetime) -> "Analyser":
        self.transactions_input_context = list(filter(
            lambda trx: start_date < trx.date < end_date, self.transactions_input))
        return self

    def filter_gt_abs_ceil(self, ceil: float) -> "Analyser":
        self.transactions_input_context = list(filter(
            lambda transaction: abs(transaction.amount) > ceil, self.transactions_input))
        return self

    # only filter are fluent so could get value in trx

    def reduce_to_sum(self):
        sum: float = 0
        for transaction in self.transactions_input_context:
            sum += transaction.amount
        return sum

    def reduce_to_card_transaction(self):
        return len(self.transactions_input_context)


def find_transaction_gt_abs_ceil(transactions_input: List[Transaction], ceil: float, start_date: datetime,
                                 end_date: datetime):
    transaction_time_filtered = filter(
        lambda trx: start_date < trx.date < end_date, transactions_input)

    return list(filter(lambda transaction: abs(transaction.amount) > ceil, transaction_time_filtered))
