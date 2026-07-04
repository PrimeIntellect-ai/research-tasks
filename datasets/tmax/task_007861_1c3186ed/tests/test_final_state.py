# test_final_state.py

import os
import pytest

def test_clean_csv_exists_and_format():
    """Verify that the clean.csv file exists and has the correct extracted data."""
    file_path = "/home/user/clean.csv"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a regular file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "0.0,10.0",
        "0.5,11.5",
        "1.0,15.0",
        "1.5,45.0",
        "2.0,80.0",
        "2.5,30.0",
        "3.0,10.0"
    ]

    actual_lines = content.split('\n')
    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        # Allow optional spaces around the comma
        actual_cleaned = actual.replace(" ", "")
        assert actual_cleaned == expected, f"Line {i+1} in {file_path} does not match expected. Expected: '{expected}', Actual: '{actual}'"

def test_analyze_rs_exists():
    """Verify that the analyze.rs file exists."""
    file_path = "/home/user/analyze.rs"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a regular file."

def test_report_txt_contents():
    """Verify that the report.txt file contains the correct calculated values."""
    file_path = "/home/user/report.txt"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a regular file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Max Power Derivative: 70.00",
        "Total Energy: 95.75"
    ]

    actual_lines = content.split('\n')
    assert len(actual_lines) >= 2, f"Expected at least 2 lines in {file_path}, found {len(actual_lines)}."

    assert actual_lines[0].strip() == expected_lines[0], f"First line of report.txt is incorrect. Expected: '{expected_lines[0]}', Actual: '{actual_lines[0]}'"
    assert actual_lines[1].strip() == expected_lines[1], f"Second line of report.txt is incorrect. Expected: '{expected_lines[1]}', Actual: '{actual_lines[1]}'"