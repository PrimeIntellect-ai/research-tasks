# test_final_state.py

import os
import pytest

def test_compiled_binary_exists():
    binary_path = "/home/user/tokenize_bayes"
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.path.isfile(binary_path), f"{binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."

def test_output_csv_correct():
    csv_path = "/home/user/output.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "token,probability",
        "data,0.400000",
        "science,0.200000",
        "processing,0.200000",
        "mining,0.200000"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {csv_path}, but found {len(lines)}."

    # We allow the order of the tokens to be exactly as they appeared in the text, 
    # which matches the C code logic.
    for i, expected_line in enumerate(expected_lines):
        assert lines[i] == expected_line, f"Line {i+1} of {csv_path} is incorrect. Expected '{expected_line}', got '{lines[i]}'."