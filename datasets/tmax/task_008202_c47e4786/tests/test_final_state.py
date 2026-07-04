# test_final_state.py

import os
import pytest

def test_flag_file_exists_and_correct():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"The file {flag_path} does not exist. You must create it."

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_password = "secure_pass_8821_alpha"

    assert content == expected_password, (
        f"The value in {flag_path} is incorrect. "
        f"Expected '{expected_password}', but got '{content}'. "
        "Make sure you correctly parsed the WAL file and applied only committed transactions."
    )