# test_final_state.py

import os
import pytest

def test_c_source_code_exists():
    """Test that the C source code file exists."""
    file_path = "/home/user/compliance_check.c"
    assert os.path.isfile(file_path), f"Source file {file_path} is missing."

def test_executable_exists():
    """Test that the compiled executable exists."""
    file_path = "/home/user/compliance_check"
    assert os.path.isfile(file_path), f"Executable {file_path} is missing. Did you compile the C code?"
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_flagged_users_log_exists():
    """Test that the output log file exists."""
    file_path = "/home/user/flagged_users.log"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing. Did you run the program?"

def test_flagged_users_log_contents():
    """Test that the output log file contains the correct results."""
    file_path = "/home/user/flagged_users.log"

    expected_lines = [
        "U2 2 5050",
        "U1 4 1300",
        "U3 4 1200"
    ]

    with open(file_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."