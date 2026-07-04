# test_final_state.py

import os
import pytest

def test_executable_exists():
    assert os.path.isfile("/home/user/health_monitor.cpp"), "The C++ source file /home/user/health_monitor.cpp is missing."
    assert os.path.isfile("/home/user/health_monitor"), "The compiled executable /home/user/health_monitor is missing."
    assert os.access("/home/user/health_monitor", os.X_OK), "The file /home/user/health_monitor is not executable."

def test_log_file_contents():
    log_path = "/home/user/health_monitor.log"
    assert os.path.isfile(log_path), f"The log file {log_path} is missing. Did the program run and create it?"

    with open(log_path, "r") as f:
        log_contents = f.read().splitlines()

    assert "RESTORED c2" in log_contents, "Log file is missing the 'RESTORED c2' entry."
    assert "RESTORED c3" in log_contents, "Log file is missing the 'RESTORED c3' entry."
    assert "RESTORED c1" not in log_contents, "Log file incorrectly contains 'RESTORED c1', but c1 was already healthy."

def test_container_statuses():
    containers = ["c1", "c2", "c3"]
    for c in containers:
        status_file = f"/home/user/containers/{c}/status.txt"
        assert os.path.isfile(status_file), f"Status file missing: {status_file}"
        with open(status_file, "r") as f:
            status = f.read().strip()
        assert status == "HEALTHY", f"Container {c} status should be 'HEALTHY', but is '{status}'."

def test_container_data_restored():
    containers = ["c1", "c2", "c3"]
    for c in containers:
        data_file = f"/home/user/containers/{c}/data.bin"
        backup_file = f"/home/user/backups/{c}_data.bin"

        assert os.path.isfile(data_file), f"Data file missing: {data_file}"
        assert os.path.isfile(backup_file), f"Backup file missing: {backup_file}"

        with open(data_file, "r") as f:
            data_content = f.read().strip()

        with open(backup_file, "r") as f:
            backup_content = f.read().strip()

        assert data_content == backup_content, f"Data file for container {c} does not match its backup. Expected '{backup_content}', got '{data_content}'."