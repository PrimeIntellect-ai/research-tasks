# test_final_state.py

import os
import subprocess
import urllib.request
import collections
import numpy as np
import time
import pytest

def test_server_py_fixed():
    server_py_path = "/app/vendor/simple_service/server.py"
    assert os.path.isfile(server_py_path), f"File {server_py_path} does not exist."
    with open(server_py_path, 'r') as f:
        content = f.read()
    assert "sys.argv[2]" not in content, "The deliberate bug (sys.argv[2]) is still present in server.py."

def test_nginx_running():
    # Check if nginx is listening on 8080
    try:
        with urllib.request.urlopen('http://127.0.0.1:8080/', timeout=2) as response:
            assert response.status == 200
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

def test_load_balancer_distribution():
    counts = collections.defaultdict(int)
    for _ in range(300):
        try:
            with urllib.request.urlopen('http://127.0.0.1:8080/', timeout=2) as response:
                body = response.read().decode('utf-8')
                # Expected response format: "Served by <port>"
                port = int(body.strip().split()[-1])
                counts[port] += 1
        except Exception as e:
            pytest.fail(f"Request to load balancer failed: {e}")

    vals = list(counts.values())
    assert len(vals) == 3, f"Expected responses from 3 distinct backends, got {len(vals)}. Counts: {dict(counts)}"

    cv = np.std(vals) / np.mean(vals)
    assert cv <= 0.05, f"CV {cv:.4f} is greater than threshold 0.05. Traffic is not evenly balanced. Counts: {dict(counts)}"

def test_log_rotation():
    log_path = "/home/user/nginx/access.log"
    rotated_log_path = "/home/user/nginx/access.log.1"
    rotate_script = "/home/user/rotate_logs.py"

    assert os.path.exists(rotate_script), f"Log rotation script {rotate_script} does not exist."
    assert os.path.exists(log_path), f"Nginx access log {log_path} does not exist."

    # Run the rotation script
    try:
        subprocess.run(["python3", rotate_script], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Log rotation script failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    assert os.path.exists(rotated_log_path), f"Rotated log file {rotated_log_path} was not created."

    # Make a new request to trigger a log write
    try:
        with urllib.request.urlopen('http://127.0.0.1:8080/', timeout=2) as response:
            assert response.status == 200
    except Exception as e:
        pytest.fail(f"Request to load balancer failed after log rotation: {e}")

    # Give Nginx a moment to write to the new log file
    time.sleep(0.5)

    assert os.path.exists(log_path), f"New log file {log_path} was not created by Nginx after rotation."
    assert os.path.getsize(log_path) > 0, f"New log file {log_path} is empty, Nginx might not have reopened its log files."