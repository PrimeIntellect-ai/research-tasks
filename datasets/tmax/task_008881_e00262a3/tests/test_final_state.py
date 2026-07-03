# test_final_state.py
import os
import json
import subprocess
import pytest

def test_deployer_go_exists():
    assert os.path.isfile("/home/user/deployer.go"), "/home/user/deployer.go does not exist. You must write the Go program."

def test_log_rotation_occurred():
    bak_path = "/home/user/logs/deploy.log.bak"
    assert os.path.isfile(bak_path), "Log rotation failed: /home/user/logs/deploy.log.bak does not exist."
    with open(bak_path, "r") as f:
        content = f.read()
    assert "VERSION v1.0.0" in content, "The backup log file does not contain the initial v1.0.0 entries."
    assert "PADDING" in content, "The backup log file does not contain the initial padding."

def test_new_deploy_log_contents():
    log_path = "/home/user/logs/deploy.log"
    assert os.path.isfile(log_path), "/home/user/logs/deploy.log does not exist."
    with open(log_path, "r") as f:
        content = f.read()

    for worker_id in [1, 2, 3]:
        expected_msg = f"WORKER {worker_id} STARTED VERSION v2.1.0"
        assert expected_msg in content, f"New log file is missing start message for worker {worker_id}: {expected_msg}"

    assert "VERSION v1.0.0" not in content, "The new log file still contains v1.0.0 entries. Log rotation may not have been performed correctly."

def test_processes_running():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps aux")

    # Ensure v1.0.0 processes are gone
    for worker_id in [1, 2, 3]:
        old_cmd = f"worker.sh {worker_id} v1.0.0"
        assert old_cmd not in output, f"Old process '{old_cmd}' is still running."

    # Ensure v2.1.0 processes are running
    for worker_id in [1, 2, 3]:
        new_cmd = f"worker.sh {worker_id} v2.1.0"
        assert new_cmd in output, f"New process '{new_cmd}' is not running."