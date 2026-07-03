# test_final_state.py

import os
import pytest

CSV_PATH = "/home/user/results.csv"

EXPECTED_OUTPUT = """4,Dave,Executive,2,120000.00
5,Eve,Engineering,2,110000.00
10,Judy,Sales,2,95000.00
7,Grace,Executive,3,90000.00"""

def test_results_csv_exists():
    """Verify that the results.csv file was generated."""
    assert os.path.isfile(CSV_PATH), f"File {CSV_PATH} was not found. Ensure the C program was compiled and executed."

def test_results_csv_content():
    """Verify the contents of the results.csv file match the expected query output."""
    assert os.path.isfile(CSV_PATH), f"File {CSV_PATH} is missing."

    with open(CSV_PATH, "r") as f:
        content = f.read().strip()

    expected_lines = EXPECTED_OUTPUT.strip().split("\n")
    actual_lines = content.split("\n")

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows, but got {len(actual_lines)} rows."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual.strip() == expected.strip(), f"Row {i+1} mismatch.\nExpected: {expected}\nGot:      {actual}"