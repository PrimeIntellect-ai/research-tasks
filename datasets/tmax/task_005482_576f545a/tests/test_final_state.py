# test_final_state.py

import os
import pytest

def test_query_c_exists():
    """Check if the C source file exists."""
    c_file = "/home/user/query.c"
    assert os.path.isfile(c_file), f"Source file {c_file} does not exist."

def test_query_executable_exists():
    """Check if the compiled executable exists and is executable."""
    exe_file = "/home/user/query"
    assert os.path.isfile(exe_file), f"Executable {exe_file} does not exist."
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

def test_results_csv_exists():
    """Check if the results.csv file exists."""
    results_file = "/home/user/results.csv"
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist."

def test_results_csv_content():
    """Check if results.csv has the correct content."""
    results_file = "/home/user/results.csv"
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist."

    with open(results_file, 'r') as f:
        content = f.read().strip()

    expected_content = "2,4\n5,4\n3,3\n10,3\n6,2\n9,1"

    # Also accept carriage returns if any
    content_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines()]

    assert content_lines == expected_lines, (
        f"Content of {results_file} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )