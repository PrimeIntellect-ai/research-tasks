# test_final_state.py

import os
import csv
import pytest

PROCESSED_FILE = "/home/user/processed_data.csv"
REJECTED_FILE = "/home/user/rejected_data.csv"

EXPECTED_HEADER = ["id", "name", "email", "phone", "rating", "comments"]

EXPECTED_PROCESSED = [
    ["101", "Alice Smith", "***@test.com", "********7890", "5", "Great service!"],
    ["201", "José García", "***@empresa.es", "*********** 456", "4", "Buen trabajo"],
    ["301", "Björn", "***@sverige.se", "********5 67", "1", "Terrible!"],
    ["302", "Müller", "***@deutschland.de", "123", "5", "Sehr gut"],
    ["303", "Empty Phone", "***@phone.com", "", "2", "No phone provided"]
]

EXPECTED_REJECTED = [
    ["102", "Bob Jones", "bob_jones_no_domain", "555-9999", "4", "Okay"],
    ["103", "Charlie", "charlie@domain.com", "987654321", "6", "Too high rating"],
    ["abc", "Bad ID", "bad@id.com", "1111", "3", "ID is letters"]
]

def read_csv_utf8(filepath):
    assert os.path.exists(filepath), f"File {filepath} does not exist."
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = list(csv.reader(f))
            return reader
    except UnicodeDecodeError:
        pytest.fail(f"File {filepath} is not strictly encoded in UTF-8.")

def test_processed_data():
    data = read_csv_utf8(PROCESSED_FILE)
    assert len(data) > 0, "processed_data.csv is empty."

    header = data[0]
    assert header == EXPECTED_HEADER, f"Header in processed_data.csv is incorrect. Got {header}"

    rows = data[1:]
    assert len(rows) == len(EXPECTED_PROCESSED), f"Expected {len(EXPECTED_PROCESSED)} rows in processed_data.csv, got {len(rows)}."

    # Check that sets of rows match (order independent)
    expected_set = {tuple(row) for row in EXPECTED_PROCESSED}
    actual_set = {tuple(row) for row in rows}

    missing = expected_set - actual_set
    extra = actual_set - expected_set

    error_msg = []
    if missing:
        error_msg.append(f"Missing expected rows: {missing}")
    if extra:
        error_msg.append(f"Unexpected extra rows: {extra}")

    assert not missing and not extra, "processed_data.csv contents do not match expected.\n" + "\n".join(error_msg)

def test_rejected_data():
    data = read_csv_utf8(REJECTED_FILE)
    assert len(data) > 0, "rejected_data.csv is empty."

    header = data[0]
    assert header == EXPECTED_HEADER, f"Header in rejected_data.csv is incorrect. Got {header}"

    rows = data[1:]
    assert len(rows) == len(EXPECTED_REJECTED), f"Expected {len(EXPECTED_REJECTED)} rows in rejected_data.csv, got {len(rows)}."

    expected_set = {tuple(row) for row in EXPECTED_REJECTED}
    actual_set = {tuple(row) for row in rows}

    missing = expected_set - actual_set
    extra = actual_set - expected_set

    error_msg = []
    if missing:
        error_msg.append(f"Missing expected rows: {missing}")
    if extra:
        error_msg.append(f"Unexpected extra rows: {extra}")

    assert not missing and not extra, "rejected_data.csv contents do not match expected.\n" + "\n".join(error_msg)