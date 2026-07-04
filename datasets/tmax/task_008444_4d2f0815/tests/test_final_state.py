# test_final_state.py

import os
import json
import pytest

def test_sre_monitor_files():
    """Check if the C source and executable exist and have correct permissions."""
    assert os.path.exists("/home/user/sre_monitor.c"), "/home/user/sre_monitor.c is missing."
    assert os.path.exists("/home/user/sre_monitor"), "/home/user/sre_monitor executable is missing."
    assert os.access("/home/user/sre_monitor", os.X_OK), "/home/user/sre_monitor is not executable."

def test_config_file():
    """Check if the configuration file has the correct contents."""
    conf_path = "/home/user/monitor.conf"
    assert os.path.exists(conf_path), "/home/user/monitor.conf is missing."
    with open(conf_path, "r") as f:
        content = f.read()
    assert "HEARTBEAT_FILE=/home/user/app_state/beat.txt" in content, "Missing HEARTBEAT_FILE in config."
    assert "DATA_DIR=/home/user/app_state" in content, "Missing DATA_DIR in config."
    assert "MIN_SPACE_MB=5" in content, "Missing MIN_SPACE_MB in config."

def test_app_state_environment():
    """Check if the mock environment directory and heartbeat file exist."""
    assert os.path.isdir("/home/user/app_state"), "/home/user/app_state directory is missing."
    assert os.path.exists("/home/user/app_state/beat.txt"), "/home/user/app_state/beat.txt is missing."

def test_status_log():
    """Validate the JSON output in the status log file."""
    log_path = "/home/user/sre_status.log"
    assert os.path.exists(log_path), "/home/user/sre_status.log is missing."

    with open(log_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) >= 1, "Log file is empty."

    try:
        last_log = json.loads(lines[-1])
    except json.JSONDecodeError:
        pytest.fail("Log file does not contain valid JSON on the last line.")

    assert "status" in last_log, "Missing 'status' key in JSON log."
    assert last_log["status"] == "UP", f"Expected status 'UP', got {last_log['status']}."

    assert "heartbeat_age_sec" in last_log, "Missing 'heartbeat_age_sec' key in JSON log."
    age = last_log["heartbeat_age_sec"]
    assert isinstance(age, int), "heartbeat_age_sec must be an integer."
    # Allow tolerance for execution delay (e.g., 20 to 60 seconds)
    assert 20 <= age <= 60, f"heartbeat_age_sec {age} is out of expected bounds (20-60)."

    assert "free_mb" in last_log, "Missing 'free_mb' key in JSON log."
    free_mb = last_log["free_mb"]
    assert isinstance(free_mb, int), "free_mb must be an integer."
    assert free_mb > 5, f"free_mb {free_mb} should be strictly greater than MIN_SPACE_MB (5)."