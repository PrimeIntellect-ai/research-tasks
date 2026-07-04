# test_final_state.py

import os
import math

def test_correlation_file_exists():
    """Test that the correlation.txt file exists."""
    file_path = "/home/user/correlation.txt"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

def test_correlation_value():
    """Test that the correlation.txt file contains the correct computed value."""
    file_path = "/home/user/correlation.txt"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    # The expected value based on the provided logs
    # LR (X): 1.0, 2.0, 3.0, 4.0, 5.0
    # ValLoss (Y): 5.0, 4.0, 3.0, 3.0, 1.0
    # Correlation = -0.959403...
    expected_value = "-0.9594"

    assert content == expected_value, f"Expected correlation value '{expected_value}', but got '{content}'."