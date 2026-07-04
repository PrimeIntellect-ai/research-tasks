# test_final_state.py

import os
import subprocess
import pytest

def test_resolution_file():
    path = "/home/user/resolution.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {path}, found {len(lines)}."
    assert lines[0] == "http://127.0.0.1:8080/timeout", f"First line of {path} is incorrect. Expected 'http://127.0.0.1:8080/timeout', got '{lines[0]}'."
    assert lines[1] == "FIXED", f"Second line of {path} is incorrect. Expected 'FIXED', got '{lines[1]}'."

def test_monitor_daemon_execution():
    script_path = "/home/user/monitor_daemon.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    try:
        result = subprocess.run(
            [script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
            text=True
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script {script_path} timed out after 15 seconds. The infinite recursion bug might not be fixed.")

    assert result.returncode == 0, f"Script {script_path} exited with non-zero code {result.returncode}. Stderr: {result.stderr}"

    status_log_path = "/home/user/status.log"
    assert os.path.isfile(status_log_path), f"Status log {status_log_path} was not created."

    with open(status_log_path, 'r') as f:
        content = f.read()

    assert "MONITORING COMPLETE" in content, f"'MONITORING COMPLETE' not found in {status_log_path}."