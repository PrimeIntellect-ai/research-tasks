# test_final_state.py

import os
import pytest

def test_source_code_exists():
    """Test that the C source code file exists."""
    file_path = "/home/user/process_requests.c"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_executable_exists():
    """Test that the compiled executable exists."""
    file_path = "/home/user/process_requests"
    assert os.path.exists(file_path), f"Executable {file_path} is missing. Did you compile your code?"
    assert os.path.isfile(file_path), f"{file_path} is not a file."
    assert os.access(file_path, os.X_OK), f"{file_path} is not executable."

def test_results_csv_content():
    """Test that the results.csv file has the correct content after processing."""
    file_path = "/home/user/results.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing. Did you run your program?"
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    expected_lines = [
        "1,12.0",
        "2,25.0",
        "1,4.0",
        "1,25.0",
        "2,12.0",
        "2,4.0"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} in {file_path} is incorrect. Expected '{expected}', got '{actual.strip()}'."