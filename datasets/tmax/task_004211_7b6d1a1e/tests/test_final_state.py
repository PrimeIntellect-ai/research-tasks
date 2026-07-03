# test_final_state.py

import os
import pytest

def test_server_go_exists():
    path = "/home/user/server.go"
    assert os.path.isfile(path), f"Expected Go server file {path} does not exist."

def test_python_script_exists():
    path = "/home/user/test_ws.py"
    assert os.path.isfile(path), f"Expected Python script {path} does not exist."

def test_migration_test_log_contents():
    path = "/home/user/migration_test.log"
    assert os.path.isfile(path), f"Log file {path} does not exist. Did the Python script run successfully?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "2,4,5,7,8"
    assert content == expected, f"Log file content is incorrect. Expected '{expected}', got '{content}'."