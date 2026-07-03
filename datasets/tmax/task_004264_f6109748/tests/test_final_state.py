# test_final_state.py

import os
import pytest

def test_go_source_file_exists():
    file_path = "/home/user/compute_variance.go"
    assert os.path.exists(file_path), f"The Go source file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_result_file_exists():
    file_path = "/home/user/result.txt"
    assert os.path.exists(file_path), f"The result file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_result_file_content():
    file_path = "/home/user/result.txt"
    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected_content = "0.00107000"
    assert content == expected_content, f"The content of {file_path} is '{content}', but expected '{expected_content}'. Make sure you are using a numerically stable algorithm and formatting to exactly 8 decimal places."