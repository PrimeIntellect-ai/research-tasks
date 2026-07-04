# test_final_state.py

import os
import pytest

def test_training_data_exists_and_correct():
    """Check that training_data.csv exists and has the correct contents."""
    file_path = "/home/user/training_data.csv"
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip().replace('\r\n', '\n')

    expected_content = "x,y\n1.5,2.1\n2.0,3.9\n3.1,6.0\n4.5,8.8\n5.0,10.1"
    assert content == expected_content, f"Contents of {file_path} do not match the expected data."

def test_cpp_file_exists():
    """Check that the C++ source file exists."""
    file_path = "/home/user/ridge_bootstrap.cpp"
    assert os.path.exists(file_path), f"File {file_path} does not exist."

def test_bootstrap_results_exists_and_correct():
    """Check that bootstrap_results.txt exists and has the exact expected output."""
    file_path = "/home/user/bootstrap_results.txt"
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip().replace('\r\n', '\n')

    expected_content = "Mean: 1.9567\nStdDev: 0.0573"
    assert content == expected_content, f"Contents of {file_path} do not match the expected output. Got:\n{content}"