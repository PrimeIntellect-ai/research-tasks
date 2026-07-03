# test_final_state.py

import os
import pytest

def test_fixed_variances_file_exists():
    """Check that the fixed_variances.txt file was created."""
    file_path = "/home/user/fixed_variances.txt"
    assert os.path.isfile(file_path), f"Missing file: {file_path}. Did you write the output to the correct path?"

def test_fixed_variances_content():
    """Check that the fixed_variances.txt file contains the correct output."""
    file_path = "/home/user/fixed_variances.txt"
    assert os.path.isfile(file_path), "Missing file: /home/user/fixed_variances.txt"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1: 0.0200",
        "2: 0.1067"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', but got '{actual}'."