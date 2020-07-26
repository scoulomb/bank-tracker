from datetime import datetime
from typing import List

from analyser.analyser import Analyser
from analyser.max_negative_transaction import find_max_negative_transaction_using_cb
from analyser.naturalia_spent_tracker import analyse_naturalia_spent
from analyser.spent import compute_all_cb_spent
from model.Transaction import Transaction
from reader.reader import deserialize_hello_bank_input_file


def analyse_by_label_content(label: str, transactions: List[Transaction], start: datetime, end: datetime):
    """"
    To print transaction
    >>> print(analyser.__str__()[0:500])
    >>> print(anylyser)
    """
    analyser = Analyser(transactions)
    analyser.filter_date(start, end).filter_by_label_contains_value(label)
    total_spent_sum = analyser.reduce_to_sum()
    average_basket = analyser.reduce_to_average()
    average_spent_per_day = total_spent_sum / (end - start).days

    print(
        f"{label} Analysis between {start} and {end}\n"
        f"Total spent is: {total_spent_sum}\n"
        f"Average basket is {average_basket}\n"
        f"Average spent per day is: {average_spent_per_day}")
    print("\n\n")


def get_positive_transactions(transactions: List[Transaction], start: datetime, end: datetime):
    analyser = Analyser(transactions)
    analyser.filter_date(start, end).filter_negative_transaction()
    print(
        f"\nPositive transactions between {start} and {end}\n")
    print(analyser)
    print("\n\n")


def get_big_transactions(transactions: List[Transaction], ceil: float, start: datetime, end: datetime):
    analyser = Analyser(transactions)
    analyser.filter_date(start, end).filter_gt_abs_ceil(ceil)
    print(
        f"\nBig transactions between {start} and {end}\n")
    print(analyser)
    print("\n\n")


def get_employer_payment(transactions: List[Transaction], start: datetime, end: datetime, business_trip_only=False):
    analyser = Analyser(transactions)
    business_trip_label_deprecated = "VIR SEPA RECU /DE COULOMBEL SYLVAIN /MOTIF  /REF "
    business_trip_label = "DEUS SAS  - DIRECTION FINANCIERE /MOTIF INV"
    salary_label = "DEUS SAS  - DIRECTION FINANCIERE /MOTIF  /REF AMAD"

    label_list = [business_trip_label_deprecated, business_trip_label]
    if not business_trip_only:
        label_list.append(salary_label)

    analyser.filter_date(start, end).filter_by_label_contains_value_list(
        label_list)

    print(
        f"\nEmployer transactions between {start} and {end} (with business trip only set to {business_trip_only})\n")
    print(analyser)
    print("\n\n")


def main():
    transactions: List[Transaction] = deserialize_hello_bank_input_file("data.csv")

    print("============ Several months analysis ==============")
    start, end = datetime(2020, 2, 1), datetime.now()
    analyse_by_label_content("NATURALIA", transactions, start, end)
    get_positive_transactions(transactions, start, end)

    origin = datetime(1989, 11, 24)
    get_big_transactions(transactions, 1500, origin, end)

    get_employer_payment(transactions, origin, end)
    get_employer_payment(transactions, origin, end, business_trip_only=True)  # match trips in cal and find ref in mail

    print("============ Last month analysis ==============")

    start, end = datetime(2020, 6, 1), datetime(2020, 7, 1)
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
