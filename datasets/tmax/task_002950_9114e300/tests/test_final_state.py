# test_final_state.py
import os
import csv
import pytest

CSV_PATH = "/home/user/audit_results.csv"

EXPECTED_ROWS = [
    ["employee", "access_time", "top_manager"],
    ["Alice CEO", "2023-01-01 00:00:00", "Alice CEO"],
    ["Charlie Director", "2023-10-05 14:00:00", "Alice CEO"],
    ["Eve Employee", "2023-10-01 10:00:00", "Alice CEO"],
    ["Grace Contractor", "2023-09-15 08:30:00", "Alice CEO"]
]

def test_audit_results_exists():
    """Test that the audit results CSV file exists."""
    assert os.path.isfile(CSV_PATH), f"Expected result file not found at {CSV_PATH}"

def test_audit_results_content():
    """Test that the audit results CSV contains the correct data."""
    with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    # Strip any potential leading/trailing whitespace from fields
    actual_rows_cleaned = [[cell.strip() for cell in row] for row in actual_rows if row]

    assert len(actual_rows_cleaned) == len(EXPECTED_ROWS), \
        f"Expected {len(EXPECTED_ROWS)} rows in the CSV, but found {len(actual_rows_cleaned)}."

    for i, (actual, expected) in enumerate(zip(actual_rows_cleaned, EXPECTED_ROWS)):
        assert actual == expected, \
            f"Row {i+1} mismatch. Expected: {expected}, Actual: {actual}"