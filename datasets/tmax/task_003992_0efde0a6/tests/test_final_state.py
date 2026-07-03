# test_final_state.py

import os
import pytest

def test_optimal_x_file():
    """Check if optimal_x.txt exists and contains the correct optimal x value."""
    file_path = "/home/user/optimizer/optimal_x.txt"
    assert os.path.exists(file_path), f"File {file_path} does not exist. Did you modify gradient_descent.py to write the output?"
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected = "42.4200"
    assert content == expected, f"Expected {file_path} to contain '{expected}', but found '{content}'."

def test_secret_file():
    """Check if secret.txt exists and contains the correct secret token."""
    file_path = "/home/user/optimizer/secret.txt"
    assert os.path.exists(file_path), f"File {file_path} does not exist. Did you run the binary with the magic number and save the output?"
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected = "TOKEN_90210_XYZ"
    assert content == expected, f"Expected {file_path} to contain '{expected}', but found '{content}'."