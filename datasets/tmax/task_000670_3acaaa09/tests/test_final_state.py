# test_final_state.py

import os
import pytest

def test_recovered_command():
    path = "/home/user/recovered_command.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "CMD_REVERSE_BASH", f"Incorrect recovered command. Found: '{content}'"

def test_cwe_id():
    path = "/home/user/cwe.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"

    with open(path, "r") as f:
        content = f.read().strip().upper()

    assert content in ["CWE-327", "CWE-326"], f"Incorrect CWE ID. Found: '{content}'"