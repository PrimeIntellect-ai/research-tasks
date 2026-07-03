# test_final_state.py

import os
import json
import stat
import subprocess
import pytest

def test_obs_profile_exists_and_content():
    path = "/home/user/.obs_profile"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()
    assert "OBS_MAX_DISK_KB=1000" in content, "OBS_MAX_DISK_KB=1000 not found in .obs_profile"
    assert "OBS_PROC_NAME=obs_target.py" in content, "OBS_PROC_NAME=obs_target.py not found in .obs_profile"

def test_obs_target_file_exists():
    path = "/home/user/obs_target.py"
    assert os.path.exists(path), f"File {path} does not exist."

def test_data_dir_and_dummy_file():
    path = "/home/user/data_dir/dummy.dat"
    assert os.path.exists(path), f"File {path} does not exist."
    size = os.path.getsize(path)
    assert size == 2097152, f"Expected {path} to be exactly 2097152 bytes (2MB), got {size} bytes."

def test_dashboard_logs_permissions():
    path = "/home/user/dashboard_logs"
    assert os.path.exists(path), f"Directory {path} does not exist."
    assert os.path.isdir(path), f"{path} is not a directory."
    stat_info = os.stat(path)
    permissions = stat.S_IMODE(stat_info.st_mode)
    assert permissions == 0o750, f"Expected permissions 0o750 for {path}, got {oct(permissions)}"

def test_collector_file_exists():
    path = "/home/user/collector.py"
    assert os.path.exists(path), f"File {path} does not exist."

def test_process_running_and_metrics_json_content():
    json_path = "/home/user/dashboard_logs/metrics.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."

    # Check process
    pid_check = subprocess.run(["pgrep", "-f", "obs_target.py"], capture_output=True, text=True)
    assert pid_check.returncode == 0, "obs_target.py is not running in the background."

    # Handle potentially multiple matching processes by taking the first one
    pids = pid_check.stdout.strip().split('\n')
    actual_pid = int(pids[0])

    # Parse JSON
    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse JSON from {json_path}")

    # Validate schema and values
    assert "target_pid" in data, "Key 'target_pid' missing from metrics.json"
    assert data["target_pid"] == actual_pid, f"Expected target_pid {actual_pid}, got {data['target_pid']}"

    assert "target_status" in data, "Key 'target_status' missing from metrics.json"
    assert data["target_status"] == "running", f"Expected target_status 'running', got '{data['target_status']}'"

    assert "data_dir_kb" in data, "Key 'data_dir_kb' missing from metrics.json"
    assert isinstance(data["data_dir_kb"], int), "data_dir_kb must be an integer"
    assert data["data_dir_kb"] >= 2048, f"Expected data_dir_kb >= 2048, got {data['data_dir_kb']}"

    assert "quota_exceeded" in data, "Key 'quota_exceeded' missing from metrics.json"
    assert data["quota_exceeded"] is True, f"Expected quota_exceeded to be True, got {data['quota_exceeded']}"