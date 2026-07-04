# test_final_state.py
import os
import csv
import pytest

def test_csv_exists():
    file_path = "/home/user/hourly_stats.csv"
    assert os.path.exists(file_path), f"The file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_csv_contents():
    file_path = "/home/user/hourly_stats.csv"

    with open(file_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"The file {file_path} is empty."

    expected_header = ["hour", "login_count", "avg_distance"]
    assert rows[0] == expected_header, f"Expected header {expected_header}, but got {rows[0]}"

    expected_data = [
        ["2023-10-12T14:00:00Z", "2", "5.00"],
        ["2023-10-12T15:00:00Z", "2", "10.00"],
        ["2023-10-13T09:00:00Z", "1", "10.00"]
    ]

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} data rows, but got {len(data_rows)}"

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}"