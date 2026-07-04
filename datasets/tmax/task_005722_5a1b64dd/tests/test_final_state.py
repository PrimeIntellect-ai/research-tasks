# test_final_state.py

import os
import pytest

def test_c_source_exists():
    """Verify that the C source code file exists."""
    assert os.path.isfile("/home/user/analyzer.c"), "C source file /home/user/analyzer.c is missing."

def test_executable_exists():
    """Verify that the compiled executable exists."""
    assert os.path.isfile("/home/user/analyzer"), "Compiled executable /home/user/analyzer is missing."
    assert os.access("/home/user/analyzer", os.X_OK), "/home/user/analyzer is not executable."

def test_csv_output():
    """Verify that the output CSV exists and contains the correct data."""
    csv_path = "/home/user/descendant_metrics.csv"
    assert os.path.isfile(csv_path), f"Output CSV file {csv_path} is missing."

    expected_lines = [
        "104,4,1",
        "101,2,2",
        "105,2,2",
        "102,1,3",
        "103,1,3"
    ]

    with open(csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"CSV output does not match expected results.\n"
        f"Expected:\n{expected_lines}\n"
        f"Actual:\n{actual_lines}"
    )