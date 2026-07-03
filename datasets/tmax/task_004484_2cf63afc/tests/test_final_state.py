# test_final_state.py

import os
import re
import stat
import pytest

def test_cracked_pin():
    """Check if the cracked PIN is correctly found and saved."""
    pin_file = "/home/user/cracked_pin.txt"
    assert os.path.isfile(pin_file), f"File {pin_file} is missing."

    with open(pin_file, 'r') as f:
        content = f.read().strip()

    assert content == "3133", f"Expected PIN '3133', but got '{content}' in {pin_file}."

def test_crack_c_exists():
    """Check if the C program source file exists."""
    c_file = "/home/user/crack.c"
    assert os.path.isfile(c_file), f"C program file {c_file} is missing."

def test_redacted_log_exists_and_permissions():
    """Check if the redacted.log exists and has 0400 permissions."""
    log_file = "/home/user/redacted.log"
    assert os.path.isfile(log_file), f"File {log_file} is missing."

    file_stat = os.stat(log_file)
    permissions = stat.S_IMODE(file_stat.st_mode)
    assert permissions == 0o400, f"Expected permissions 0400 for {log_file}, but got {oct(permissions)}."

def test_redacted_log_content():
    """Check if the sensitive tokens are redacted correctly in redacted.log."""
    log_file = "/home/user/redacted.log"
    assert os.path.isfile(log_file), f"File {log_file} is missing."

    with open(log_file, 'r') as f:
        content = f.read()

    # Check that REDACTED was inserted
    assert "Authorization: Bearer REDACTED" in content, \
        "The string 'Authorization: Bearer REDACTED' was not found in the redacted log."

    # Check that no 64-character hex strings remain after Bearer
    unredacted_match = re.search(r"Bearer [0-9a-fA-F]{64}", content)
    assert unredacted_match is None, \
        f"Found unredacted token in {log_file}: {unredacted_match.group(0)}"

def test_redacted_log_preserves_other_content():
    """Ensure that the rest of the log content is preserved."""
    log_file = "/home/user/redacted.log"
    assert os.path.isfile(log_file), f"File {log_file} is missing."

    with open(log_file, 'r') as f:
        content = f.read()

    assert "GET /api/v1/users HTTP/1.1" in content, "Missing original content 'GET /api/v1/users HTTP/1.1'."
    assert "POST /api/v1/update HTTP/1.1" in content, "Missing original content 'POST /api/v1/update HTTP/1.1'."
    assert '{"status": "active"}' in content, "Missing original JSON payload."
    assert "GET /public/info HTTP/1.1" in content, "Missing original content 'GET /public/info HTTP/1.1'."