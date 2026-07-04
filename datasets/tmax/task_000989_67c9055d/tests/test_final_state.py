# test_final_state.py
import os
import pytest

def test_impute_go_exists():
    """Test that the Go source file was created."""
    file_path = '/home/user/impute.go'
    assert os.path.exists(file_path), f"Required Go source file {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} exists but is not a regular file."

def test_result_file_exists():
    """Test that the result file was generated."""
    file_path = '/home/user/result.txt'
    assert os.path.exists(file_path), f"Required result file {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} exists but is not a regular file."

def test_result_content():
    """Test that the result file contains the correct computed sum."""
    file_path = '/home/user/result.txt'
    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected_sum = "122500.0000"
    assert content == expected_sum, f"Result file content is incorrect. Expected '{expected_sum}', got '{content}'."