# test_final_state.py
import os
import pytest

RESULT_PATH = '/home/user/result.txt'

def test_result_file_exists():
    assert os.path.exists(RESULT_PATH), f"Result file {RESULT_PATH} is missing. Did you write the output to the correct location?"

def test_result_value():
    with open(RESULT_PATH, 'r') as f:
        content = f.read().strip()

    assert content == "3", f"Expected the shortest path length to be 3, but got '{content}'."