# test_final_state.py
import os
import csv
import pytest

def test_output_csv_exists():
    csv_path = "/home/user/manager_project_hours.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"{csv_path} is not a regular file."

def test_output_csv_content():
    csv_path = "/home/user/manager_project_hours.csv"
    assert os.path.exists(csv_path), "Cannot check content because CSV file is missing."

    expected_rows = [
        ["Alice", "Alpha", "45"],
        ["Alice", "Beta", "35"],
        ["Bob", "Alpha", "30"],
        ["Bob", "Beta", "15"],
        ["Charlie", "Alpha", "5"],
        ["Charlie", "Beta", "20"]
    ]
    expected_header = ["manager_name", "project_name", "total_hours"]

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("CSV file is empty.")

        assert header == expected_header, f"Expected header {expected_header}, but got {header}."

        actual_rows = list(reader)
        assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}."

        for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
            assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}."