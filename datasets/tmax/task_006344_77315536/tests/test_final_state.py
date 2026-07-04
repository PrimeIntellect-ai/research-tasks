# test_final_state.py

import os
import stat
import pytest

def test_crack_token_go_exists():
    """Verify that the Go script was created at the specified path."""
    script_path = "/home/user/crack_token.go"
    assert os.path.isfile(script_path), f"Expected Go script at {script_path} does not exist."

def test_valid_auth_log_exists():
    """Verify that the valid_auth.log file exists."""
    log_path = "/home/user/valid_auth.log"
    assert os.path.isfile(log_path), f"Expected log file at {log_path} does not exist."

def test_valid_auth_log_content():
    """Verify that the content of valid_auth.log is exactly 'admin:secret73'."""
    log_path = "/home/user/valid_auth.log"
    assert os.path.isfile(log_path), "Log file does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "admin:secret73", f"Expected content 'admin:secret73', but got '{content}'."

def test_valid_auth_log_permissions():
    """Verify that the permissions of valid_auth.log are exactly 0600."""
    log_path = "/home/user/valid_auth.log"
    assert os.path.isfile(log_path), "Log file does not exist."

    file_stat = os.stat(log_path)
    # Extract the permission bits
    permissions = stat.S_IMODE(file_stat.st_mode)

    assert permissions == 0o600, f"Expected permissions 0600, but got {oct(permissions)}."