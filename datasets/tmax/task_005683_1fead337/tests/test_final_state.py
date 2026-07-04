# test_final_state.py

import os
import pytest

def test_regression_failures_file_exists():
    path = "/home/user/regression_failures.txt"
    assert os.path.isfile(path), f"The expected output file {path} does not exist."

def test_regression_failures_contents():
    path = "/home/user/regression_failures.txt"
    assert os.path.isfile(path), f"The expected output file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "data_02.h5",
        "data_03.h5"
    ]

    assert lines == expected_lines, (
        f"Contents of {path} do not match the expected output. "
        f"Expected {expected_lines}, but got {lines}."
    )