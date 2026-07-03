# test_final_state.py

import os
import time
import subprocess
import pytest

def test_deploy_script_executable():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"{deploy_script} does not exist or is not a file."
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable."

def test_exporter_running():
    pid_file = "/home/user/exporter.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid PID."
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} (from {pid_file}) is not running.")

def test_metrics_prom():
    metrics_file = "/home/user/dashboard/metrics.prom"

    # Give the exporter a moment to write the file if it just started
    for _ in range(30):
        if os.path.isfile(metrics_file):
            break
        time.sleep(0.1)

    assert os.path.isfile(metrics_file), f"Metrics file {metrics_file} is missing."

    with open(metrics_file, "r") as f:
        content = f.read()

    expected_lines = [
        'mount_active{path="/home/user/mounts/app_data"} 1',
        'mount_active{path="/home/user/mounts/backup"} 1',
        'mount_active{path="/home/user/mounts/offline"} 0'
    ]

    for line in expected_lines:
        assert line in content, f"Expected metric '{line}' not found in {metrics_file}"

def test_idempotency():
    pid_file = "/home/user/exporter.pid"
    with open(pid_file, "r") as f:
        old_pid_str = f.read().strip()

    old_pid = int(old_pid_str)

    # Run deploy.sh again
    deploy_script = "/home/user/deploy.sh"
    result = subprocess.run([deploy_script], capture_output=True, text=True)
    assert result.returncode == 0, f"{deploy_script} failed on second run. Error: {result.stderr}"

    time.sleep(0.5) # Wait briefly for the script to update the PID file

    with open(pid_file, "r") as f:
        new_pid_str = f.read().strip()

    assert new_pid_str.isdigit(), f"PID file {pid_file} does not contain a valid PID after redeploy."
    new_pid = int(new_pid_str)

    assert old_pid != new_pid, "PID did not change after redeploy. Service lifecycle failed (not restarted)."

    try:
        os.kill(new_pid, 0)
    except OSError:
        pytest.fail(f"New process with PID {new_pid} is not running after redeploy.")