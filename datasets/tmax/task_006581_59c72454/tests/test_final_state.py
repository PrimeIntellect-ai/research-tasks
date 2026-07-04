# test_final_state.py

import os
import pytest

def test_tune_cpp_exists_and_non_empty():
    """Test that the C++ source file exists and is not empty."""
    cpp_path = '/home/user/tune.cpp'
    assert os.path.exists(cpp_path), f"File {cpp_path} does not exist."
    assert os.path.isfile(cpp_path), f"Path {cpp_path} is not a file."
    assert os.path.getsize(cpp_path) > 0, f"File {cpp_path} is empty."

def test_result_txt_matches_expected():
    """Test that the result.txt file contains the correct output."""
    result_path = '/home/user/result.txt'
    expected_path = '/tmp/expected_result.txt'

    assert os.path.exists(result_path), f"File {result_path} does not exist. Did you run your C++ program and write to the correct path?"
    assert os.path.isfile(result_path), f"Path {result_path} is not a file."

    with open(result_path, 'r') as f:
        result_content = f.read().strip()

    with open(expected_path, 'r') as f:
        expected_content = f.read().strip()

    assert result_content == expected_content, f"Content of {result_path} ('{result_content}') does not match expected output ('{expected_content}')."