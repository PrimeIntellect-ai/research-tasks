# test_final_state.py

import os
import pytest

APP_DIR = "/home/user/app"
GO_BINARY = os.path.join(APP_DIR, "vnc-monitor")
ENV_FILE = os.path.join(APP_DIR, "monitor.env")
LOG_FILE = os.path.join(APP_DIR, "status.log")

def test_go_binary_exists_and_executable():
    assert os.path.isfile(GO_BINARY), f"Compiled Go binary {GO_BINARY} does not exist. Did you compile it?"
    assert os.access(GO_BINARY, os.X_OK), f"Go binary {GO_BINARY} is not executable."

def test_env_file_exists():
    assert os.path.isfile(ENV_FILE), f"Environment file {ENV_FILE} does not exist."

def test_status_log_exists():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist. The application may not have run successfully."

def test_status_log_content():
    # The expected output string based on the Go source code requirements
    expected_content = "STATUS: OK | TZ: Etc/UTC | LANG: C.UTF-8 | VNC_TARGET: 127.0.0.1:5901"

    with open(LOG_FILE, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Log file content does not match expected output.\nExpected: {expected_content}\nGot: {content}"