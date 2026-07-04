# test_final_state.py

import os
import pytest

def test_results_csv_exists_and_correct():
    results_file = "/home/user/results.csv"
    assert os.path.isfile(results_file), f"The output file {results_file} does not exist."

    expected_lines = [
        "University of British Columbia,100",
        "University of Toronto,90",
        "University of Waterloo,80"
    ]

    with open(results_file, "r") as f:
        # Read lines, stripping trailing whitespace
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {results_file} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )

def test_process_data_c_exists():
    c_file = "/home/user/process_data.c"
    assert os.path.isfile(c_file), f"The source code file {c_file} does not exist."

def test_process_data_executable_exists():
    executable = "/home/user/process_data"
    assert os.path.isfile(executable), f"The compiled executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"The file {executable} is not executable."