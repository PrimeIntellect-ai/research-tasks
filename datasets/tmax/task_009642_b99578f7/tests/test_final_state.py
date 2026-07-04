# test_final_state.py

import os
import pytest

def test_crashing_id_txt():
    path = "/home/user/crashing_id.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "2899", f"Expected crashing ID to be '2899', but found '{content}' in {path}"

def test_filter_users_py_exists():
    path = "/home/user/filter_users.py"
    assert os.path.isfile(path), f"Missing script: {path}. You need to write a script that filters the users."

def test_safe_users_txt():
    path = "/home/user/safe_users.txt"
    assert os.path.isfile(path), f"Missing file: {path}. Did you run your filter script?"

    expected_safe_users = ["10", "450", "1999", "2147"]

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_safe_users, f"Expected safe users to be {expected_safe_users}, but found {lines} in {path}"