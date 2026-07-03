# test_final_state.py

import os
import subprocess
import pytest

def test_script_exists():
    """Check if the edge_monitor.py script exists and is a file."""
    script_path = "/home/user/edge_monitor.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist or is not a file."

def test_log_directory_exists():
    """Check if the edge_logs directory was created."""
    log_dir = "/home/user/edge_logs"
    assert os.path.isdir(log_dir), f"Directory {log_dir} does not exist."

def test_log_files_exist():
    """Check if the log rotation created the expected files."""
    expected_files = [
        "status.log",
        "status.log.1",
        "status.log.2",
        "status.log.3"
    ]
    for filename in expected_files:
        filepath = os.path.join("/home/user/edge_logs", filename)
        assert os.path.isfile(filepath), f"Log file {filepath} is missing. Log rotation may not be configured correctly."

def test_log_content():
    """Check if the current log file contains the expected output."""
    log_path = "/home/user/edge_logs/status.log"
    with open(log_path, "r") as f:
        content = f.read()
    assert "Ping successful" in content, f"Expected 'Ping successful' in {log_path}, but got: {content}"

def test_container_stopped():
    """Check that the apptainer instance 'iot_worker' is stopped."""
    result = subprocess.run(
        ["apptainer", "instance", "list"],
        capture_output=True,
        text=True,
        check=False
    )
    assert "iot_worker" not in result.stdout, "Apptainer instance 'iot_worker' is still running. Cleanup failed."