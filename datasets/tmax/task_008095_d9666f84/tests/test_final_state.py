# test_final_state.py

import os
import json
import subprocess
import time

def test_status_json_exists_and_valid():
    """Verify that status.json exists and contains valid JSON."""
    status_file = '/home/user/status.json'
    assert os.path.exists(status_file), f"{status_file} does not exist."

    with open(status_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{status_file} does not contain valid JSON."

    assert isinstance(data, dict), f"JSON in {status_file} must be an object (dict)."

def test_status_json_content():
    """Verify that the JSON correctly identifies active and inactive PIDs."""
    pids_file = '/home/user/monitored_pids.txt'
    status_file = '/home/user/status.json'

    assert os.path.exists(pids_file), f"{pids_file} is missing."
    with open(pids_file, 'r') as f:
        pids = [line.strip() for line in f if line.strip()]

    with open(status_file, 'r') as f:
        data = json.load(f)

    for pid in pids:
        assert pid in data, f"PID {pid} is missing from {status_file}."

        is_active = os.path.isdir(f"/proc/{pid}")
        expected_status = "active" if is_active else "inactive"

        assert data[pid] == expected_status, f"PID {pid} should be '{expected_status}', but got '{data[pid]}'."

def test_health_monitor_running():
    """Verify that the health_monitor process is running in the background."""
    try:
        ps_output = subprocess.check_output(['ps', '-e', '-o', 'comm='], text=True)
    except subprocess.CalledProcessError:
        assert False, "Failed to execute 'ps' command."

    processes = [line.strip() for line in ps_output.splitlines()]
    assert "health_monitor" in processes, "The 'health_monitor' process is not running in the background."