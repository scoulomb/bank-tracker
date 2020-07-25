from datetime import datetime
from typing import List

from analyser.find_transaction_gt_abs_ceil import find_transaction_gt_abs_ceil
from analyser.max_negative_transaction import find_max_negative_transaction_using_cb
from analyser.money_input import get_positive_transaction
from analyser.naturalia_spent_tracker import analyse_naturalia_spent
from analyser.spent import compute_all_cb_spent
from model import Transaction
from reader.reader import deserialize_hello_bank_input_file


def main():
    transactions: List[Transaction] = deserialize_hello_bank_input_file("data.csv")

    print("============ Several month analysis ==============")
    start, end = datetime(2020, 2, 1), datetime.now()

    result = analyse_naturalia_spent(transactions, start, end)
    print(
        f"NATURALIA Analysis between {start} and {end}\n"
        f"Total spent is: {result[0]}\n"
        f"Average spent per day is: {result[1]}\n"
        f"Average basket is {result[2]}")
    print(
        f"\npostive transactions between {start} and {end}\n")
    labels = [trx.label for trx in get_positive_transaction(transactions, start, end)]
    for l in labels:
        print(l)

    origin = datetime(1989, 11, 24)
    print(
        f"\nBig transactions between {origin} and {end}\n")
    trx = find_transaction_gt_abs_ceil(transactions, 1500, origin, end)
    print(len(trx))
    for t in trx:
        print(t.date, t.label, t.amount)

    print("============ Last month analysis ==============")

    start, end = datetime(2020, 6, 20), datetime(2020, 7, 10)
    result = compute_all_cb_spent(transactions, start, end)
    print(
        f"All spent Analysis WITH CB between {start} and{end}\n"
        f"Total spent is: {result}\n")

    result = find_max_negative_transaction_using_cb(transactions, start, end)
    print(
        f"Highest trx WITH CB between {start} and {end}\n"
        f"{result.label} with amount {result.amount}\n")

    result = analyse_naturalia_spent(transactions, start, end)
    print(
        f"Naturalia spent analysis between {start} and {end}\n"
        f"Total spent is: {result[0]}\n"
        f"Average spent per day is: {result[1]}\n"
        f"Average basket is {result[2]}")

    # we can deduce how much is spent at Naturalia from total cb spent


if __name__ == "__main__":
    main()
