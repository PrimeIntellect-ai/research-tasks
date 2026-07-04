# test_final_state.py

import os
import pytest

def test_cwe_file_correct():
    path = "/home/user/workspace/cwe.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you create it?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "CWE-22", f"Expected '{path}' to contain 'CWE-22', but found '{content}'."

def test_audit_success_file_correct():
    path = "/home/user/workspace/audit_success.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The exploit did not successfully write the file."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "EXPLOITED", f"Expected '{path}' to contain 'EXPLOITED', but found '{content}'."