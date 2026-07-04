# test_final_state.py

import os
import csv
import pytest

def test_summary_csv_exists():
    """Check that summary.csv was generated."""
    assert os.path.isfile("/home/user/summary.csv"), "/home/user/summary.csv does not exist."

def test_summary_csv_content():
    """Check that summary.csv contains the correct aggregated, sorted, and paginated results."""
    expected = [
        ["Marketing", "110000"],
        ["Sales", "100000"]
    ]

    actual = []
    with open("/home/user/summary.csv", "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # skip empty lines if any
                actual.append(row)

    assert actual == expected, f"Expected {expected}, but got {actual}. Ensure correct aggregation, filtering (>50000), sorting, and limits."

def test_report_py_parameterization():
    """Check that report.py uses parameterized queries (initBindings)."""
    with open("/home/user/report.py", "r") as f:
        content = f.read()

    assert "initBindings" in content or "initBindings=" in content, "The script must use initBindings to pass the MIN_SALARY parameter securely."
    assert "MIN_SALARY" in content, "The script must still define and use MIN_SALARY."