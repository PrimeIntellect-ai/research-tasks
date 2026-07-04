# test_final_state.py

import os
import pytest

def test_result_file_exists():
    """Test that the result.txt file exists."""
    file_path = "/home/user/result.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing. Did your script create it?"
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_result_content():
    """Test that the result.txt file contains the correct Wasserstein distance."""
    file_path = "/home/user/result.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected_value = "0.5898"
    assert content == expected_value, f"Expected the result to be '{expected_value}', but found '{content}'."

def test_analyze_script_exists():
    """Test that the analyze.py script exists."""
    file_path = "/home/user/analyze.py"
    assert os.path.exists(file_path), f"File {file_path} is missing. You must write your code in this file."
    assert os.path.isfile(file_path), f"{file_path} is not a file."