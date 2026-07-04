# test_final_state.py

import os
import pytest

def test_executable_exists():
    path = "/home/user/etl_processor"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile the C program?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_processed_csv_exists():
    path = "/home/user/processed.csv"
    assert os.path.isfile(path), f"Output file {path} does not exist. Did you run the pipeline and save the output?"

def test_processed_csv_content():
    path = "/home/user/processed.csv"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    expected_lines = [
        "1,200",
        "2,NA",
        "3,NA",
        "4,NA",
        "5,56",
        "6,0"
    ]

    with open(path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, but found {len(actual_lines)}. Did you skip the header correctly?"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."