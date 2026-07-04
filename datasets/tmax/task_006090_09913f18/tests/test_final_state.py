# test_final_state.py

import os
import pytest

def test_permissions_log():
    path = "/home/user/permissions.log"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    expected = "-rwxr-xr--"
    assert content == expected, f"Expected permissions '{expected}', but got '{content}'"

def test_vulnerability_log():
    path = "/home/user/vulnerability.log"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    expected = "https://malicious.example.com/redirect?url=http://trusted.com"
    assert content == expected, f"Expected vulnerability URL '{expected}', but got '{content}'"

def test_cert_status_log():
    path = "/home/user/cert_status.log"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    expected = "VALID"
    assert content == expected, f"Expected cert status '{expected}', but got '{content}'"