# test_final_state.py

import os
import pytest

def test_solution_go_exists():
    """Verify that the user created the solution.go file."""
    path = "/home/user/solution.go"
    assert os.path.exists(path), f"Missing required file: {path}"
    assert os.path.isfile(path), f"Expected a file, but found a directory: {path}"

def test_corrected_results_exists():
    """Verify that the corrected_results.txt file exists."""
    path = "/home/user/corrected_results.txt"
    assert os.path.exists(path), f"Missing required file: {path}"
    assert os.path.isfile(path), f"Expected a file, but found a directory: {path}"

def test_corrected_results_content():
    """Verify that the corrected_results.txt file contains the correct sample variance calculations."""
    path = "/home/user/corrected_results.txt"
    expected_lines = [
        "2.50",
        "1.00",
        "1.00",
        "4.00",
        "0.50"
    ]

    with open(path, "r") as f:
        content = f.read().splitlines()

    # Filter out empty lines
    content = [line.strip() for line in content if line.strip()]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines of output, but got {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual == expected, f"Line {i+1} is incorrect. Expected '{expected}', but got '{actual}'."