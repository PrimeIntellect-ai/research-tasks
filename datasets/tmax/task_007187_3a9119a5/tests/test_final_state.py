# test_final_state.py

import os
import pytest

def test_processor_c_exists():
    path = "/home/user/processor.c"
    assert os.path.isfile(path), f"Source file not found: {path}"

def test_processor_executable_exists():
    path = "/home/user/processor"
    assert os.path.isfile(path), f"Executable not found: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_output_csv():
    path = "/home/user/output.csv"
    assert os.path.isfile(path), f"Output file not found: {path}"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "user_id,score",
        "4,60.00",
        "6,60.00",
        "7,50.00",
        "8,50.00"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, but found {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual}'"