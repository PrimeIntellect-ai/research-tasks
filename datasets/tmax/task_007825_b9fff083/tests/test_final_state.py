# test_final_state.py
import os
import time
import base64
import subprocess
import pytest

def test_runner_executable():
    runner_path = "/home/user/auto_provision_runner"
    assert os.path.isfile(runner_path), f"{runner_path} does not exist."
    assert os.access(runner_path, os.X_OK), f"{runner_path} is not executable."

def test_daemon_executable():
    daemon_path = "/home/user/provision_daemon.sh"
    assert os.path.isfile(daemon_path), f"{daemon_path} does not exist."
    assert os.access(daemon_path, os.X_OK), f"{daemon_path} is not executable."

def test_daemon_running():
    output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
    assert "provision_daemon.sh" in output, "provision_daemon.sh is not running in the background."

def test_processing_pipeline():
    job_file = "/home/user/job_queue.txt"
    log_file = "/home/user/processed_tokens.log"

    # Test case 1
    cluster1 = "prod-eu-central"
    port1 = "8443"
    expected_token1 = base64.b64encode(f"{cluster1}:{port1}:n".encode('utf-8')).decode('utf-8')

    with open(job_file, "w") as f:
        f.write(f"export CLUSTER_NAME={cluster1}\n")
        f.write(f"export BASE_PORT={port1}\n")

    # Wait up to 10 seconds for the file to be processed
    for _ in range(10):
        if not os.path.exists(job_file):
            break
        time.sleep(1)

    assert not os.path.exists(job_file), f"{job_file} was not deleted by the daemon. Polling might not be working."
    assert os.path.exists(log_file), f"{log_file} was not created."

    with open(log_file, "r") as f:
        lines = f.read().splitlines()
    assert len(lines) >= 1, f"{log_file} is empty."
    assert lines[-1].strip() == expected_token1, f"Expected token {expected_token1} not found at the end of {log_file}."

    # Test case 2
    cluster2 = "dev-us-east"
    port2 = "9090"
    expected_token2 = base64.b64encode(f"{cluster2}:{port2}:n".encode('utf-8')).decode('utf-8')

    with open(job_file, "w") as f:
        f.write(f"export CLUSTER_NAME={cluster2}\n")
        f.write(f"export BASE_PORT={port2}\n")

    # Wait up to 10 seconds for the second file to be processed
    for _ in range(10):
        if not os.path.exists(job_file):
            break
        time.sleep(1)

    assert not os.path.exists(job_file), f"{job_file} was not deleted by the daemon on the second run."

    with open(log_file, "r") as f:
        lines = f.read().splitlines()
    assert len(lines) >= 2, f"{log_file} does not have enough lines appended."
    assert lines[-1].strip() == expected_token2, f"Expected token {expected_token2} not found at the end of {log_file}."