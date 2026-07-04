# test_final_state.py
import os
import csv
import pytest

def test_deadlock_report_exists():
    csv_path = "/home/user/deadlock_report.csv"
    assert os.path.isfile(csv_path), f"The file {csv_path} does not exist. Did you run your script and generate the output?"

def test_deadlock_report_content():
    csv_path = "/home/user/deadlock_report.csv"
    assert os.path.isfile(csv_path), f"The file {csv_path} does not exist."

    expected_header = ["tx_id", "wait_start_ms", "cycle_rank"]
    expected_rows = [
        ["TX-42", "1620000100", "1"],
        ["TX-55", "1620000150", "2"],
        ["TX-61", "1620000200", "3"]
    ]

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"{csv_path} is empty.")

        assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}."

        rows = list(reader)
        assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(rows)}."

        for i, (expected, actual) in enumerate(zip(expected_rows, rows)):
            assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."