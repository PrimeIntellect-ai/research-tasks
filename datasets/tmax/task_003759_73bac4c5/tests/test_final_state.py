# test_final_state.py
import os
import re
import pytest

def test_best_parameters_file_exists():
    """Test that the best_parameters.txt file exists."""
    file_path = "/home/user/best_parameters.txt"
    assert os.path.exists(file_path), f"The file {file_path} does not exist. Did the C++ program run successfully?"
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_best_parameters_content():
    """Test that the best_parameters.txt file contains the correct A, D, and MSE."""
    file_path = "/home/user/best_parameters.txt"
    assert os.path.exists(file_path), f"The file {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content != "", f"The file {file_path} is empty."

    # Split by whitespace
    parts = content.split()
    assert len(parts) == 3, f"Expected exactly 3 space-separated numbers in {file_path}, but found {len(parts)}."

    # Expected values
    expected_A = "3.1200"
    expected_D = "0.5300"
    expected_MSE = "0.0000"

    assert parts[0] == expected_A, f"Expected A={expected_A}, but got {parts[0]}."
    assert parts[1] == expected_D, f"Expected D={expected_D}, but got {parts[1]}."

    # MSE might be very small, but the requirement specifically asks for 4 decimal places
    # So it should be exactly "0.0000"
    assert parts[2] == expected_MSE, f"Expected MSE={expected_MSE}, but got {parts[2]}."

def test_cpp_source_file_exists():
    """Test that the fit_model.cpp file exists."""
    file_path = "/home/user/fit_model.cpp"
    assert os.path.exists(file_path), f"The file {file_path} does not exist. You must write the C++ program."