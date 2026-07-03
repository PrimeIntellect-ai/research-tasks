# test_final_state.py

import os
import pytest
import csv

def test_validate_go_exists():
    path = "/home/user/validate.go"
    assert os.path.isfile(path), f"Expected Go script {path} does not exist."

def test_cleaned_metrics_csv():
    path = "/home/user/cleaned_metrics.csv"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

    expected_data = [
        ["id", "category", "abs_error"],
        ["1", "A", "0.50"],
        ["3", "A", "1.80"],
        ["5", "B", "0.10"],
        ["6", "C", "0.00"]
    ]

    with open(path, "r", newline="") as f:
        reader = csv.reader(f)
        actual_data = list(reader)

    # Check header
    assert len(actual_data) > 0, "The cleaned_metrics.csv file is empty."
    assert actual_data[0] == expected_data[0], f"Header mismatch. Expected {expected_data[0]}, got {actual_data[0]}"

    # Sort both to ensure order doesn't fail the test if they joined differently, 
    # though usually order is preserved. Let's just compare sorted rows.
    expected_rows = sorted(expected_data[1:], key=lambda x: int(x[0]))
    actual_rows = sorted(actual_data[1:], key=lambda x: int(x[0]) if x[0].isdigit() else 0)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."