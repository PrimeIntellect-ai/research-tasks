# test_final_state.py

import os
import pytest

def test_exploit_source_exists():
    """Verify that the student created the exploit source file."""
    exploit_path = "/home/user/exploit.c"
    assert os.path.exists(exploit_path), f"Missing required file: {exploit_path}. You must write your exploit source code here."
    assert os.path.isfile(exploit_path), f"Expected {exploit_path} to be a file, but found a directory."

def test_pwned_log_exists_and_correct():
    """Verify that the exploit successfully executed and wrote the correct session ID to the log."""
    log_path = "/home/user/pwned.log"

    assert os.path.exists(log_path), f"File {log_path} does not exist. The exploit may not have run or failed to trigger the command injection."
    assert os.path.isfile(log_path), f"Expected {log_path} to be a file, but found a directory."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_session_id = "SEC-998877-TOK"
    assert content == expected_session_id, f"Expected {log_path} to contain exactly '{expected_session_id}', but found '{content}'. Check your log parsing and command injection payload."