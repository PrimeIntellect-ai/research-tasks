# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    source_path = "/home/user/process_citations.c"
    assert os.path.isfile(source_path), f"C source file not found at {source_path}"

def test_executable_exists_and_is_executable():
    executable_path = "/home/user/process_citations"
    assert os.path.isfile(executable_path), f"Executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_results_file_content():
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    expected_content = (
        "Longest Chain Length: 5\n"
        "Top Paper 2019: 101 (1 citations)\n"
        "Top Paper 2020: 103 (3 citations)\n"
        "Top Paper 2021: 105 (2 citations)\n"
        "Top Paper 2022: 111 (2 citations)"
    )

    with open(results_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {results_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )