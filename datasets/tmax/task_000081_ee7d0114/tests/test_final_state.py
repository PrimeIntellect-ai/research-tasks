# test_final_state.py

import os
import pytest

def test_result_file_exists():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing. Did you save the result?"

def test_result_content():
    result_path = "/home/user/result.txt"
    if not os.path.isfile(result_path):
        pytest.fail(f"File {result_path} is missing.")

    with open(result_path, "r") as f:
        content = f.read().strip()

    # The variance of integers 1 to 100 is (100^2 - 1)/12 = 833.25
    # Since the sequence numbers are shifted by a constant, the variance remains exactly 833.25.
    expected = "833.25"
    assert content == expected, f"Expected variance to be '{expected}', but got '{content}'."