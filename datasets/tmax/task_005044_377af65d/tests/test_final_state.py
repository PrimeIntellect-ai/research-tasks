# test_final_state.py

import os
import re
import time
import subprocess
import pytest

def test_deploy_script_exists_and_executable():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"Deployment script {deploy_script} does not exist."
    assert os.access(deploy_script, os.X_OK), f"Deployment script {deploy_script} is not executable."

def test_nginx_temp_dir_exists():
    temp_dir = "/home/user/nginx_temp"
    assert os.path.isdir(temp_dir), f"Nginx temp directory {temp_dir} was not created."

def test_system_performance_and_correctness():
    # Give the services a moment to start if the agent just ran the script
    time.sleep(2)

    try:
        # Run wrk load test against the Nginx port specified in the image
        result = subprocess.run(
            ["wrk", "-t4", "-c100", "-d10s", "http://127.0.0.1:8080/"],
            capture_output=True, text=True, timeout=20
        )
    except FileNotFoundError:
        pytest.fail("wrk command not found. Ensure wrk is installed in the environment.")
    except subprocess.TimeoutExpired:
        pytest.fail("wrk load test timed out.")

    output = result.stdout

    # Check for errors (Non-2xx/3xx or connection errors)
    errors = re.search(r"Non-2xx or 3xx responses:\s+(\d+)", output)
    if errors and int(errors.group(1)) > 0:
        pytest.fail(f"Found {errors.group(1)} Bad Gateway or other non-2xx/3xx errors.")

    socket_errors = re.search(r"Socket errors:\s+(.*)", output)
    if socket_errors:
        pytest.fail(f"Socket errors detected: {socket_errors.group(1)}")

    # Extract requests per second
    rps_match = re.search(r"Requests/sec:\s+([\d\.]+)", output)
    assert rps_match is not None, f"Could not parse Requests/sec from wrk output:\n{output}"

    rps = float(rps_match.group(1))
    threshold = 2000.0

    assert rps >= threshold, f"Throughput too low: achieved {rps} RPS, expected >= {threshold} RPS."