# test_final_state.py
import os
import pytest

def test_result_file_exists():
    result_file = '/home/user/result.txt'
    assert os.path.exists(result_file), f"The result file {result_file} does not exist."
    assert os.path.isfile(result_file), f"{result_file} is not a valid file."

def test_result_value():
    result_file = '/home/user/result.txt'
    with open(result_file, 'r') as f:
        content = f.read().strip()

    assert content == "12", f"Expected dominant frequency to be 12, but got '{content}'."