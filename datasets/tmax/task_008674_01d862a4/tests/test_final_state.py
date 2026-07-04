# test_final_state.py

import os
import pytest

def test_process_c_exists():
    assert os.path.isfile("/home/user/process.c"), "The C source file /home/user/process.c does not exist."

def test_report_csv_exists():
    assert os.path.isfile("/home/user/report.csv"), "The output file /home/user/report.csv does not exist."

def test_report_csv_content():
    report_path = "/home/user/report.csv"
    assert os.path.isfile(report_path), f"The output file {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1,3,20.00",
        "2,0,5.00",
        "3,1,110.00",
        "4,4,10.00"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in report.csv, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."