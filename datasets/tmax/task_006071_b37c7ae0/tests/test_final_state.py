# test_final_state.py

import os
import subprocess
import pytest

def test_restore_manager_exists():
    path = "/home/user/restore_manager.py"
    assert os.path.exists(path), f"Missing file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

def test_restore_success_log_exists_and_content():
    path = "/home/user/restore_success.log"
    assert os.path.exists(path), f"Missing file: {path}. The script did not generate the log file."
    assert os.path.isfile(path), f"Not a file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "RESTORE_COMPLETED_SUCCESSFULLY_99283"
    assert content == expected, f"Incorrect content in {path}. Expected '{expected}', got '{content}'"

def test_db_mock_not_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "db_mock.py"]).decode("utf-8")
        running = bool(output.strip())
    except subprocess.CalledProcessError:
        running = False

    assert not running, "db_mock.py process is still running. It should have been terminated cleanly."

def test_socket_does_not_exist():
    path = "/home/user/db_ready.sock"
    assert not os.path.exists(path), f"Socket file still exists: {path}. The db_mock.py process was not cleanly terminated."