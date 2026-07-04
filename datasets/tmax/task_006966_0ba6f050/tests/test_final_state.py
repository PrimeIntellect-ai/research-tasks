# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    """Verify that the C source file exists."""
    file_path = "/home/user/solve_model.c"
    assert os.path.isfile(file_path), f"Expected C source file {file_path} is missing."

def test_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    file_path = "/home/user/solve_model"
    assert os.path.isfile(file_path), f"Expected executable {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_results_csv_content():
    """Verify that the results.csv file exists and contains the correct output."""
    file_path = "/home/user/results.csv"
    assert os.path.isfile(file_path), f"Expected results file {file_path} is missing."

    expected_lines = [
        "SequenceID,FinalY",
        "seqA1,7.18",
        "seqB2,2.39",
        "seqC3,14.37",
        "seqD4,0.60"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    # Normalize by stripping whitespace
    content = [line.strip() for line in content if line.strip()]

    assert content == expected_lines, (
        f"Content of {file_path} does not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {content}"
    )