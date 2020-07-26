import json
from datetime import datetime
from typing import List, Dict, Any

from model.Transaction import Transaction


class Analyser:
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

    def filter_by_label_contains_value(self, values_to_be_contained: str) -> "Analyser":
        self.transactions_input_context = list(filter(
            lambda transaction: values_to_be_contained in transaction.label, self.transactions_input_context))
        return self

    def filter_negative_transaction(self):
        self.transactions_input_context = list(filter(
            lambda transaction: transaction.amount > 0, self.transactions_input_context))
        return self

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
