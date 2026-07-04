# test_final_state.py

import os
import stat
import time
import requests
import pytest
import subprocess

def test_files_exist_and_permissions():
    assert os.path.isfile("/home/user/deploy_gateway.go"), "deploy_gateway.go is missing"

    rollout_path = "/home/user/rollout.sh"
    assert os.path.isfile(rollout_path), "rollout.sh is missing"

    # Check if rollout.sh is executable
    st = os.stat(rollout_path)
    assert bool(st.st_mode & stat.S_IXUSR), "rollout.sh is not executable"

def test_http_endpoint_unauthorized():
    url = "http://127.0.0.1:8080/deploy"

    # Missing header
    try:
        response = requests.post(url, timeout=2)
        assert response.status_code == 401, f"Expected 401 for missing header, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go application: {e}")

    # Wrong header
    try:
        response = requests.post(url, headers={"X-Voice-Auth": "123456"}, timeout=2)
        assert response.status_code == 401, f"Expected 401 for wrong header, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go application: {e}")

def test_http_endpoint_authorized_and_rollout():
    url = "http://127.0.0.1:8080/deploy"

    # Clean up log file if it exists to ensure we see fresh results
    log_file = "/home/user/deploy_log.txt"
    if os.path.exists(log_file):
        os.remove(log_file)

    try:
        response = requests.post(url, headers={"X-Voice-Auth": "839201"}, timeout=5)
        assert response.status_code == 200, f"Expected 200 OK for correct header, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Go application: {e}")

    # Wait a brief moment for the script to finish writing
    time.sleep(1)

    assert os.path.isfile(log_file), "deploy_log.txt was not created after successful deployment"

    with open(log_file, "r") as f:
        content = f.read().strip().split('\n')

    expected_lines = [
        "DEPLOYED TO: 192.168.1.10",
        "DEPLOYED TO: 192.168.1.11",
        "DEPLOYED TO: 10.0.0.5"
    ]

    assert len(content) == 3, f"Expected 3 lines in deploy_log.txt, got {len(content)}"
    for expected, actual in zip(expected_lines, content):
        assert expected == actual, f"Expected log line '{expected}', but got '{actual}'"

def test_rollout_script_error_handling(tmp_path):
    # Temporarily move servers.txt to test error handling
    servers_path = "/app/servers.txt"
    backup_path = "/app/servers.txt.bak"

    if os.path.exists(servers_path):
        os.rename(servers_path, backup_path)

    log_file = "/home/user/deploy_log.txt"
    if os.path.exists(log_file):
        os.remove(log_file)

    try:
        # Run the rollout script directly
        result = subprocess.run(["/home/user/rollout.sh"], capture_output=True)
        assert result.returncode == 1, f"Expected rollout.sh to exit with code 1 when servers.txt is missing, got {result.returncode}"

        assert os.path.isfile(log_file), "deploy_log.txt was not created during error handling"
        with open(log_file, "r") as f:
            content = f.read().strip()

        assert "ERROR: servers.txt missing" in content, f"Expected error message in log, got: {content}"
    finally:
        # Restore servers.txt
        if os.path.exists(backup_path):
            os.rename(backup_path, servers_path)