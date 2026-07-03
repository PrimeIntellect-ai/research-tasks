# test_final_state.py

import os
import pytest

def test_cpp_source_exists():
    """Verify that the C++ source file exists."""
    cpp_file = "/home/user/analyze.cpp"
    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."

def test_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    exe_file = "/home/user/analyze"
    assert os.path.isfile(exe_file), f"Executable {exe_file} is missing."
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

def test_output_file_exists():
    """Verify that the output CSV file exists."""
    output_file = "/home/user/top_accounts.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

def test_output_file_content():
    """Verify that the output CSV file contains exactly the expected top 3 accounts."""
    output_file = "/home/user/top_accounts.csv"
    with open(output_file, "r") as f:
        # Read lines, strip whitespace, and ignore empty lines
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "7,4",
        "1,3",
        "4,3"
    ]

    assert len(lines) == 3, f"Expected exactly 3 lines in {output_file}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."