# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_requests.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_audit_log_exists_and_correct():
    log_path = "/home/user/audit_log.csv"
    assert os.path.isfile(log_path), f"Audit log {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "req1.b64,AUTH_OK,CLEAN",
        "req2.b64,AUTH_FAIL,CLEAN",
        "req3.b64,AUTH_OK,THREAT_DETECTED",
        "req4.b64,AUTH_FAIL,THREAT_DETECTED"
    ]

    # The instructions specify sorting alphabetically by filename
    expected_lines.sort()

    assert lines == expected_lines, f"Audit log content is incorrect. Expected {expected_lines}, but got {lines}."