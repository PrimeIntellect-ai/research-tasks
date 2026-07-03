# test_final_state.py

import os
import csv
import pytest

def test_violations_csv_exists():
    csv_path = "/home/user/violations.csv"
    assert os.path.isfile(csv_path), f"The expected output file {csv_path} does not exist."

def test_violations_csv_contents():
    csv_path = "/home/user/violations.csv"
    assert os.path.isfile(csv_path), f"The expected output file {csv_path} does not exist."

    expected_rows = [
        ["timestamp", "user_name", "department_name", "resource_id", "action"],
        ["2023-10-01T10:05:00Z", "Charlie", "Engineering", "200", "WRITE"],
        ["2023-10-01T10:10:00Z", "Alice", "Engineering", "300", "READ"]
    ]

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) > 0, f"The file {csv_path} is empty."

    # Check header
    assert actual_rows[0] == expected_rows[0], f"Header mismatch in {csv_path}. Expected: {expected_rows[0]}, Got: {actual_rows[0]}"

    # Check data
    assert actual_rows == expected_rows, f"Content mismatch in {csv_path}. Expected {expected_rows}, but got {actual_rows}."