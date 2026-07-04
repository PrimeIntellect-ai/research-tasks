# test_final_state.py

import os
import pytest

def test_executable_exists():
    """Test that the compiled C++ program exists and is executable."""
    executable_path = "/home/user/graph_query"
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_results_file_exists():
    """Test that the query results file exists."""
    results_path = "/home/user/query_results.txt"
    assert os.path.isfile(results_path), f"Results file {results_path} is missing."

def test_results_content():
    """Test that the query results file contains the correct output."""
    results_path = "/home/user/query_results.txt"
    assert os.path.isfile(results_path), f"Results file {results_path} is missing."

    with open(results_path, "r") as f:
        content = f.read().strip().splitlines()

    # Strip carriage returns just in case
    content = [line.strip() for line in content if line.strip()]

    expected = ["Person_2", "Person_4"]

    assert content == expected, (
        f"Query results do not match expected output.\n"
        f"Expected: {expected}\n"
        f"Actual: {content}"
    )