# test_final_state.py

import os
import stat
import pytest

def test_cracker_cpp_exists():
    path = "/home/user/cracker.cpp"
    assert os.path.isfile(path), f"Missing file: {path}. You must write your solution in this file."

def test_compromised_accounts_output():
    path = "/home/user/compromised_accounts.txt"
    assert os.path.isfile(path), f"Missing file: {path}. Your program must create this file."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "sysadmin:admin:http://evil.com/steal",
        "devteam:hunter2:https://phish.net/login"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, but found {len(lines)}."

    for expected in expected_lines:
        assert expected in lines, f"Missing expected output line in {path}: '{expected}'"

def test_ssh_key_backup_permissions():
    path = "/home/user/ssh_key_backup"
    assert os.path.isfile(path), f"Missing file: {path}. Did you delete it?"

    st = os.stat(path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o400, f"Permissions for {path} should be 400 (owner read-only), but got {oct(permissions)}"