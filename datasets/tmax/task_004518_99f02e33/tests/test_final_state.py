# test_final_state.py

import os
import pytest

def test_minimal_bug_csv():
    file_path = "/home/user/minimal_bug.csv"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected = "2.0,3.000001"
    assert content == expected, f"Expected {file_path} to contain '{expected}', but got '{content}'."

def test_bug_cause_txt():
    file_path = "/home/user/bug_cause.txt"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected = "acos"
    assert content == expected, f"Expected {file_path} to contain '{expected}', but got '{content}'."