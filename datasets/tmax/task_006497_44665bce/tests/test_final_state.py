# test_final_state.py

import os
import pytest

def test_decrypted_flag():
    flag_path = "/home/user/decrypted_flag.txt"
    assert os.path.isfile(flag_path), f"The file {flag_path} does not exist. Did you run the analyzer script and save its output?"

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{malware_analyzed_successfully_8842}"
    assert content == expected_flag, f"The decrypted flag in {flag_path} is incorrect. Expected '{expected_flag}', but got '{content}'."