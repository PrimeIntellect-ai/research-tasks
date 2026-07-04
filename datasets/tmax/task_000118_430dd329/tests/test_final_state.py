# test_final_state.py

import os
import pytest

def test_deadlock_txt_exists():
    file_path = "/home/user/deadlock.txt"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a regular file."

def test_deadlock_txt_contents():
    file_path = "/home/user/deadlock.txt"
    expected_content = "T02,T04,T06,T08,T03"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"The contents of {file_path} do not match the expected deadlock cycle. Expected '{expected_content}', got '{content}'."