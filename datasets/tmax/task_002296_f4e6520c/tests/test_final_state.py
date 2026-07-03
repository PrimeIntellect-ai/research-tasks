# test_final_state.py

import os
import pytest

def test_recovered_csv_exists():
    path = "/home/user/recovered.csv"
    assert os.path.isfile(path), f"Expected file {path} does not exist. Did you write the output to the correct location?"

def test_recovered_csv_content():
    path = "/home/user/recovered.csv"
    assert os.path.isfile(path), "Cannot check content because recovered.csv is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1,10.5000",
        "2,20.2500",
        "3,30.1250",
        "4,40.8750"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in recovered.csv, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in recovered.csv is incorrect. Expected '{expected}', got '{actual}'."

def test_recover_go_exists():
    path = "/home/user/recover.go"
    assert os.path.isfile(path), f"Expected file {path} does not exist. Did you create the Go script as requested?"