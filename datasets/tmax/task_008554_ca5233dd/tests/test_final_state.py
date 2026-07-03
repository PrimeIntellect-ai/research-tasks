# test_final_state.py
import os
import pytest

def test_c_program_exists():
    """Test that the C program process_svd.c exists."""
    file_path = "/home/user/sim_data/process_svd.c"
    assert os.path.isfile(file_path), f"The C program file {file_path} does not exist."

def test_result_file_exists():
    """Test that the result.txt file exists."""
    file_path = "/home/user/sim_data/result.txt"
    assert os.path.isfile(file_path), f"The result file {file_path} does not exist. Did you run the compiled program?"

def test_result_file_content():
    """Test that the result.txt file contains the correct largest singular value."""
    file_path = "/home/user/sim_data/result.txt"
    assert os.path.isfile(file_path), f"The result file {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_value = "25.4624"
    assert content == expected_value, f"The content of {file_path} is '{content}', expected '{expected_value}'."