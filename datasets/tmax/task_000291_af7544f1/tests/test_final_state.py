# test_final_state.py

import os
import pytest

def test_source_file_exists():
    source_path = "/home/user/graph_etl.c"
    assert os.path.isfile(source_path), f"Source file {source_path} does not exist."

def test_binary_exists_and_executable():
    binary_path = "/home/user/graph_etl"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_results_file_exists_and_correct():
    results_path = "/home/user/results.csv"
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."

    expected_output = [
        "10,12",
        "13,15",
        "13,17",
        "18,17"
    ]

    with open(results_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_output, (
        f"Content of {results_path} does not match expected output.\n"
        f"Expected: {expected_output}\n"
        f"Actual: {actual_lines}"
    )