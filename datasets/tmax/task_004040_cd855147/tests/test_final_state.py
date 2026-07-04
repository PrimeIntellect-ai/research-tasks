# test_final_state.py

import os
import pytest

def test_operator_script_exists():
    path = "/home/user/operator.py"
    assert os.path.isfile(path), f"Operator script not found at {path}"

def test_operator_log_exists():
    path = "/home/user/operator.log"
    assert os.path.isfile(path), f"Operator log not found at {path}. Did the operator run and create it?"

def test_operator_log_contents():
    path = "/home/user/operator.log"
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "[EXEC] Starting db",
        "[STATE] db is ready",
        "[EXEC] Starting app",
        "[WARN] app crashed, restarting",
        "[EXEC] Starting app",
        "[WARN] app crashed, restarting",
        "[EXEC] Starting app"
    ]

    assert lines == expected_lines, f"Log contents do not match expected sequence. Found: {lines}"

def test_app_state():
    path = "/home/user/app.state"
    assert os.path.isfile(path), f"App state file not found at {path}. Did the app run?"
    with open(path, "r") as f:
        count = int(f.read().strip())

    assert count == 3, f"Expected app to have run exactly 3 times, but state indicates {count} runs."