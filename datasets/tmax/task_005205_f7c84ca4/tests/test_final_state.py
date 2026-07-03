# test_final_state.py

import os
import pytest

def test_api_key_recovered():
    api_key_path = "/home/user/api_key.txt"
    assert os.path.isfile(api_key_path), f"The file {api_key_path} does not exist."

    with open(api_key_path, "r") as f:
        content = f.read().strip()

    assert content == "SEC_9988_xyz123", "The recovered API key in api_key.txt is incorrect."

def test_result_file_accurate():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"The file {result_path} does not exist. Did you run the fixed script?"

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "3000000000000000.06", f"The calculated total in {result_path} is incorrect. Expected '3000000000000000.06', got '{content}'."