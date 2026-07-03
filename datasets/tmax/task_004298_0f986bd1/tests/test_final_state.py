# test_final_state.py

import os
import pytest

def test_alerts_log():
    """Test that alerts.log exists and contains the correct malicious paths."""
    log_path = "/home/user/logs/alerts.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist."
    assert os.path.isfile(log_path), f"Path {log_path} is not a file."

    with open(log_path, "r") as f:
        content = f.read().splitlines()

    expected_paths = {"../../etc/passwd", "/var/log/syslog"}
    actual_paths = set(line.strip() for line in content if line.strip())

    assert expected_paths.issubset(actual_paths), f"Expected malicious paths {expected_paths} not found in {log_path}. Found: {actual_paths}"

def test_safe_log():
    """Test that safe.log exists and contains the correct safe paths."""
    log_path = "/home/user/logs/safe.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist."
    assert os.path.isfile(log_path), f"Path {log_path} is not a file."

    with open(log_path, "r") as f:
        content = f.read().splitlines()

    expected_paths = {"valid_data_1.csv", "valid_data_2.txt"}
    actual_paths = set(line.strip() for line in content if line.strip())

    assert expected_paths.issubset(actual_paths), f"Expected safe paths {expected_paths} not found in {log_path}. Found: {actual_paths}"

def test_safepipe_c_exists():
    """Test that safepipe.c exists."""
    c_path = "/home/user/workspace/safepipe.c"
    assert os.path.exists(c_path), f"File {c_path} does not exist."
    assert os.path.isfile(c_path), f"Path {c_path} is not a file."

def test_safepipe_executable_exists():
    """Test that the compiled safepipe executable exists and is executable."""
    exe_path = "/home/user/workspace/safepipe"
    assert os.path.exists(exe_path), f"File {exe_path} does not exist."
    assert os.path.isfile(exe_path), f"Path {exe_path} is not a file."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_monitor_sh_exists():
    """Test that monitor.sh exists."""
    script_path = "/home/user/workspace/monitor.sh"
    assert os.path.exists(script_path), f"File {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."
    # The prompt doesn't strictly say it must be executable, but it's a bash script that is run.
    # We will just check existence as per prompt.