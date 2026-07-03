# test_final_state.py

import os
import requests
import pytest

def test_gatewayd_installed():
    """Verify that gatewayd was installed to the correct local directory."""
    expected_path = "/home/user/local/bin/gatewayd"
    assert os.path.isfile(expected_path), f"Expected installed binary at {expected_path} is missing."
    assert os.access(expected_path, os.X_OK), f"The binary at {expected_path} is not executable."

def test_scripts_exist_and_executable():
    """Verify that the supervisor and deploy scripts exist and are executable."""
    supervisor_path = "/home/user/supervisor.sh"
    deploy_path = "/home/user/deploy.sh"

    assert os.path.isfile(supervisor_path), f"Supervisor script {supervisor_path} is missing."
    assert os.access(supervisor_path, os.X_OK), f"Supervisor script {supervisor_path} is not executable."

    assert os.path.isfile(deploy_path), f"Deploy script {deploy_path} is missing."
    assert os.access(deploy_path, os.X_OK), f"Deploy script {deploy_path} is not executable."

def test_gateway_health_endpoint():
    """
    Verify that the socat port forwarder is running on port 9090, 
    forwarding to the gatewayd service on 8080, and that the service 
    is authorized via the environment variable.
    """
    url = "http://127.0.0.1:9090/health"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the gateway via socat at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"
    assert "OK - Authorized" in response.text, f"Expected 'OK - Authorized' in response body, got: {response.text}"