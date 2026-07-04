# test_final_state.py

import os
import pytest

def test_clean_calibration_csv():
    file_path = "/home/user/clean_calibration.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

    expected_lines = [
        "x,y,status",
        "1.0,2.2,valid",
        "2.0,4.1,valid",
        "3.0,6.0,valid",
        "6.0,12.1,valid"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    # Allow for variations in float formatting (e.g., 1 vs 1.0) but standardizing is safer.
    # However, exact string matching of the expected lines is standard for this task's simple CSV.
    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        # Remove any trailing commas or spaces
        actual_clean = actual.strip()
        assert actual_clean == expected, f"Line {i+1} in {file_path} is incorrect. Expected '{expected}', got '{actual_clean}'."

def test_report_txt():
    file_path = "/home/user/report.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

    expected_lines = [
        "1.9857",
        "0.1429",
        "0.0571"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == 3, f"Expected exactly 3 lines in {file_path}, found {len(content)}."

    labels = ["Slope (m)", "Y-intercept (b)", "Mean Absolute Error (MAE)"]
    for i, (actual, expected, label) in enumerate(zip(content, expected_lines, labels)):
        actual_val = actual.strip()
        assert actual_val == expected, f"{label} on line {i+1} is incorrect. Expected '{expected}', got '{actual_val}'."