import json
from datetime import datetime
from typing import List, Dict, Any

from model.Transaction import Transaction


class Analyser:
    """"
    Analyse transaction using fluent interface: https://en.wikipedia.org/wiki/Fluent_interface
    """
    def __init__(self, transactions_input: List[Transaction]):
        self.transactions_input = transactions_input
        self.transactions_input_context = transactions_input

    def __str__(self) -> str:
        out_dict = self.to_dict()
        return json.dumps(out_dict, indent=3)

    def to_dict(self):
        out_dict: Dict[str, Any] = {"count": len(self.transactions_input_context), "items": []}
        for index, transaction in enumerate(self.transactions_input_context):
            content_dict: Dict[str, str] = {"id": index, "date": transaction.date.strftime("%Y-%m-%d"),
                                            "label": transaction.label,
                                            "amount": transaction.amount}
            out_dict["items"].append(content_dict)
        return out_dict

    def reset(self):
        self.transactions_input_context = self.transactions_input

    def get_transactions(self) -> List[Transaction]:
        return self.transactions_input_context

    def filter_date(self, start_date: datetime, end_date: datetime) -> "Analyser":
        self.transactions_input_context = list(filter(
            lambda trx: start_date < trx.date < end_date, self.transactions_input_context))
        return self

    def filter_gt_abs_ceil(self, ceil: float) -> "Analyser":
        self.transactions_input_context = list(filter(
            lambda transaction: abs(transaction.amount) > ceil, self.transactions_input_context))
        return self

    def filter_by_label_contains_value(self, value_to_be_contained: str) -> "Analyser":
        self.transactions_input_context = list(filter(
            lambda transaction: value_to_be_contained in transaction.label, self.transactions_input_context))
        return self

    def filter_by_label_contains_value_list(self, values_to_be_contained: List[str]) -> "Analyser":
        def filter_func(transaction: Transaction):
            for value in values_to_be_contained:
                if value in transaction.label:
                    return True
            return False

        self.transactions_input_context = list(filter(
            filter_func, self.transactions_input_context))
        return self

    def filter_negative_transaction(self):
        self.transactions_input_context = list(filter(
            lambda transaction: transaction.amount > 0, self.transactions_input_context))
        return self

    def filter_positive_transaction(self):
        self.transactions_input_context = list(filter(
            lambda transaction: transaction.amount < 0, self.transactions_input_context))
        return self

    def filter_by_kind(self, kind: str):
        self.transactions_input_context = list(filter(
            lambda transaction: transaction.kind == kind, self.transactions_input_context))
        return self

    def sort_transactions_by_amount(self) -> "Analyser":
        self.transactions_input_context.sort(key=lambda trx: trx.amount)
        return self

    def head(self, n: int) -> "Analyser":
        self.transactions_input_context = self.transactions_input_context[0:n]
        return self

    def highest_spent_transaction(self) -> Transaction:
        return min(self.transactions_input_context, key=lambda trx: trx.amount)




    def reduce_to_sum(self) -> float:
        sum: float = 0
        for transaction in self.transactions_input_context:
            sum += transaction.amount
        return sum

    def reduce_to_count(self) -> int:
        return len(self.transactions_input_context)

    def reduce_to_average(self) -> float:
        count = self.reduce_to_count()
        if count > 0:
            return self.reduce_to_sum() / self.reduce_to_count()
        return 0


