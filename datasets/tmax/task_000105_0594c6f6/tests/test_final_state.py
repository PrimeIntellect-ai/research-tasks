# test_final_state.py

import os
import pytest

def test_server_executable_exists():
    server_path = "/home/user/service/server"
    assert os.path.isfile(server_path), f"The compiled executable {server_path} is missing."
    assert os.access(server_path, os.X_OK), f"The file {server_path} is not executable."

def test_leak_fixed_log_exists():
    log_path = "/home/user/leak_fixed.log"
    assert os.path.isfile(log_path), f"The verification log {log_path} was not created. Did you run /home/user/verify.sh?"

def test_leak_fixed_log_success():
    log_path = "/home/user/leak_fixed.log"
    assert os.path.isfile(log_path), f"The verification log {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content.startswith("SUCCESS"), f"Expected {log_path} to indicate SUCCESS, but got: {content}"