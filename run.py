from datetime import datetime
from typing import List

from analyser.analyser import Analyser
from model.Transaction import Transaction
from reader.reader import deserialize_hello_bank_input_file


def analyse_by_label_content(label: str, transactions: List[Transaction], start: datetime, end: datetime) -> float:
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
    return total_spent_sum


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


def year_analysis(transactions: List[Transaction]):
    print("============ Year analysis ==============")
    start, end = datetime(2020, 2, 1), datetime.now()
    analyse_by_label_content("NATURALIA", transactions, start, end)
    get_positive_transactions(transactions, start, end)

    origin = datetime(1989, 11, 24)
    get_big_transactions(transactions, 1500, origin, end)

    get_employer_payment(transactions, origin, end)
    get_employer_payment(transactions, origin, end, business_trip_only=True)  # match trips in cal and find ref in mail


def month_analysis(transactions: List[Transaction]):
    """"
    CB spent = highest trx + Naturalia + epsilon
    """
    print("============ Last month analysis ==============")
    start, end = datetime(2020, 6, 15), datetime(2020, 7, 15)

    analyser = Analyser(transactions)
    analyser.filter_date(start, end).filter_by_kind("PAIEMENT CB")
    print(
        f"\nSpent between {start} and {end} with CB is {analyser.reduce_to_sum()}")
    # print(analyser.highest_spent_transaction())
    print(
        f"Where top transaction are\n")
    print(analyser.sort_transactions_by_amount().head(2))
    print("\nWhere spent includes Naturalia =>")
    analyse_by_label_content("NATURALIA", transactions, start, end)


def main():
    transactions: List[Transaction] = deserialize_hello_bank_input_file("data.csv")
    year_analysis(transactions)
    month_analysis(transactions)


if __name__ == "__main__":
    main()
