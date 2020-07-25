import csv
import datetime
from typing import List

from model.Transaction import Transaction


def make_date_from_string(input_string: str) -> datetime:
    date_tuple = (input_string.split("/"))
    date: datetime = datetime.datetime(int(date_tuple[2]), int(date_tuple[1]), int(date_tuple[0]))
    return date


def deserialize_hello_bank_input_file(file_path: str) -> List[Transaction]:
    transaction_list: List[Transaction] = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # skip header
        for row in reader:
            date: datetime = make_date_from_string(row[0])
            transaction_list.append(
                Transaction(date, row[1], row[2], row[3], float(row[4].replace(",", ".").replace(" ", ""))))
    return transaction_list
    # could use yield
