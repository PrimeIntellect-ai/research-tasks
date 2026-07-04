# test_final_state.py

import os
import stat
import pytest

def test_credential_extraction():
    key_path = "/home/user/compromised_key.txt"
    assert os.path.exists(key_path), f"File {key_path} does not exist."

    with open(key_path, "r") as f:
        content = f.read().strip()

    expected_key = "sk-test-8f7d6c5b4a392817"
    assert content == expected_key, f"Expected {key_path} to contain '{expected_key}', but found '{content}'."

def test_access_control():
    pem_path = "/home/user/private.pem"
    assert os.path.exists(pem_path), f"File {pem_path} does not exist."

    file_stat = os.stat(pem_path)
    permissions = stat.S_IMODE(file_stat.st_mode)

    assert permissions == 0o600, f"Expected permissions of {pem_path} to be 600, but got {oct(permissions)}."

def test_integrity_verification():
    status_path = "/home/user/integrity_status.txt"
    assert os.path.exists(status_path), f"File {status_path} does not exist."

    with open(status_path, "r") as f:
        content = f.read().strip()

    expected_status = "VALID"
    assert content == expected_status, f"Expected {status_path} to contain '{expected_status}', but found '{content}'."