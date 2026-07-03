# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

def test_nginx_success_rate():
    """
    Send 100 GET requests to Nginx and calculate the success rate.
    Threshold: Success rate >= 0.95
    """
    url = "http://127.0.0.1:8080/api/data"
    total_requests = 100
    successful_responses = 0

    for _ in range(total_requests):
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.getcode() == 200:
                    data = response.read().decode('utf-8')
                    try:
                        json_data = json.loads(data)
                        if json_data.get("status") == "ok" and json_data.get("data") == "vendored_app_active":
                            successful_responses += 1
                    except json.JSONDecodeError:
                        pass
        except (urllib.error.HTTPError, urllib.error.URLError):
            pass

    success_rate = successful_responses / total_requests
    assert success_rate >= 0.95, f"Success rate {success_rate} is below the threshold of 0.95. Expected 200 OK with correct JSON payload."

def test_start_backend_script_exists():
    """Check if the agent created the start_backend.py script."""
    path = "/home/user/start_backend.py"
    assert os.path.isfile(path), f"File {path} does not exist. The agent was required to create it."

def test_verify_deployment_script_exists():
    """Check if the agent created the verify_deployment.py script."""
    path = "/home/user/verify_deployment.py"
    assert os.path.isfile(path), f"File {path} does not exist. The agent was required to create it."

def test_success_rate_file_exists_and_valid():
    """Check if the success_rate.txt file exists and contains a valid float."""
    path = "/home/user/success_rate.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did the agent run verify_deployment.py?"

    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        agent_success_rate = float(content)
    except ValueError:
        pytest.fail(f"Content of {path} is not a valid float: '{content}'")

    assert 0.0 <= agent_success_rate <= 1.0, f"Success rate in {path} must be between 0.0 and 1.0, got {agent_success_rate}"