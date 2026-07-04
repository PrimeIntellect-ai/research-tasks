# test_final_state.py

import os
import csv
import pytest

def test_violations_csv_exists():
    """Check if the violations.csv file exists."""
    file_path = "/home/user/violations.csv"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist. Did you run your script to generate it?"

def test_violations_csv_content():
    """Check if the violations.csv file contains the correct headers and data in the correct order."""
    file_path = "/home/user/violations.csv"
    if not os.path.isfile(file_path):
        pytest.fail(f"The file {file_path} does not exist.")

    expected_rows = [
        ["EmployeeID", "Name", "Department"],
        ["http://example.org/emp1", "Alice Smith", "Engineering"],
        ["http://example.org/emp5", "Eve Brown", "IT"]
    ]

    with open(file_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) > 0, "The violations.csv file is empty."

    # Check headers
    assert actual_rows[0] == expected_rows[0], f"Headers in violations.csv are incorrect. Expected {expected_rows[0]}, got {actual_rows[0]}"

    # Check data
    assert actual_rows == expected_rows, (
        "The contents of violations.csv do not match the expected output. "
        "Ensure you are finding employees with access to both FinancialSystem and HRSystem "
        "who are not in the Executive department, and that the rows are sorted alphabetically by EmployeeID."
    )