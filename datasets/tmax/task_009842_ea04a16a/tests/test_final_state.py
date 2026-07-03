# test_final_state.py

import os
import pytest

def test_total_sum_file_exists():
    assert os.path.isfile("/home/user/total_sum.txt"), "/home/user/total_sum.txt is missing. Did the script run successfully?"

def test_total_sum_value():
    with open("/home/user/total_sum.txt", "r") as f:
        content = f.read().strip()

    expected_sum = "51000.00000250"

    assert content == expected_sum, f"Expected total sum to be exactly '{expected_sum}', but got '{content}'."

def test_process_script_exists():
    assert os.path.isfile("/home/user/process.sh"), "/home/user/process.sh is missing."