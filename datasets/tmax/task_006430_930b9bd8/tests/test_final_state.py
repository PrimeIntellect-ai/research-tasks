# test_final_state.py

import os
import pytest

def test_app_fw_compiled():
    """Verify that the C daemon has been compiled and is executable."""
    path = "/home/user/app_fw"
    assert os.path.isfile(path), f"The compiled executable {path} is missing. Did you compile app_fw.c?"
    assert os.access(path, os.X_OK), f"The file {path} is not executable."

def test_test_fw_exp_exists():
    """Verify that the Expect script was created."""
    path = "/home/user/test_fw.exp"
    assert os.path.isfile(path), f"The expect script {path} is missing."

def test_start_sh_fixed():
    """Verify that start.sh has been modified to include a wait loop for port 7777."""
    path = "/home/user/start.sh"
    assert os.path.isfile(path), f"The file {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    # Check for loop constructs and port 7777
    has_loop = "while" in content or "until" in content
    has_port = "7777" in content

    assert has_loop, "start.sh does not appear to contain a loop (while/until) to wait for the port."
    assert has_port, "start.sh does not appear to check for port 7777."

def test_success_log():
    """Verify that success.log exists and contains the correct token."""
    path = "/home/user/success.log"
    assert os.path.isfile(path), f"The file {path} is missing. The script may have failed to execute or write the output."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_token = "TOKEN: MIGRATION_AUTH_994827"
    assert expected_token in content, f"success.log does not contain the expected token '{expected_token}'. Found: {content}"