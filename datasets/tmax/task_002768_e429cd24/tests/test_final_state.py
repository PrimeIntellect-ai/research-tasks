# test_final_state.py
import os
import pytest

def test_query_c_exists():
    """Check if the C source file was created."""
    c_path = "/home/user/query.c"
    assert os.path.isfile(c_path), f"C source file {c_path} does not exist."

def test_result_file_exists_and_content():
    """Check if the result.txt file exists and has the correct output."""
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist. The C program may not have been run or failed to create it."

    with open(result_path, "r") as f:
        # Read lines, strip whitespace to handle potential trailing newlines/spaces
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = ["2", "6", "7", "8", "9"]

    assert lines == expected_lines, (
        f"Content of {result_path} is incorrect.\n"
        f"Expected lines: {expected_lines}\n"
        f"Actual lines: {lines}"
    )