# test_final_state.py

import os
import pytest
import math

def test_svd_results_file_exists():
    """Test that the svd_results.txt file exists."""
    results_file = "/home/user/svd_results.txt"
    assert os.path.exists(results_file), f"File {results_file} does not exist. Did you run your Rust program?"
    assert os.path.isfile(results_file), f"Path {results_file} is not a file."

def test_svd_results_content():
    """Test that the svd_results.txt file contains the correct top 3 singular values."""
    results_file = "/home/user/svd_results.txt"
    assert os.path.exists(results_file), f"File {results_file} does not exist."

    with open(results_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {results_file}, found {len(lines)}."

    expected_values = [11.6669, 2.2858, 2.0729]

    for i, (actual_str, expected) in enumerate(zip(lines, expected_values)):
        try:
            actual = float(actual_str)
        except ValueError:
            pytest.fail(f"Line {i+1} in {results_file} is not a valid float: '{actual_str}'")

        # Check to 4 decimal places
        assert math.isclose(actual, expected, abs_tol=1e-4), \
            f"Value on line {i+1} is incorrect. Expected {expected:.4f}, got {actual:.4f}."

        # Also check format if possible, but float comparison is safer
        # Let's ensure it has exactly 4 decimal places
        parts = actual_str.split('.')
        if len(parts) == 2:
            assert len(parts[1]) == 4, f"Value '{actual_str}' on line {i+1} is not formatted to exactly 4 decimal places."
        else:
            pytest.fail(f"Value '{actual_str}' on line {i+1} is not formatted to exactly 4 decimal places.")