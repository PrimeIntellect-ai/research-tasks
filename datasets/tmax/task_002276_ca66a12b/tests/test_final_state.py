# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_routes_file():
    """Verify that the routes.txt file was correctly generated."""
    routes_path = '/home/user/routes.txt'
    assert os.path.isfile(routes_path), f"The routes file {routes_path} is missing."
    with open(routes_path, 'r') as f:
        content = f.read()

    assert "app1:192.168.1.10" in content, "Route for app1 is missing or incorrect."
    assert "app2:192.168.1.11" in content, "Route for app2 is missing or incorrect."
    assert "db_main:10.0.0.5" in content, "Route for db_main is missing or incorrect."

def test_daemon_health():
    """Test the /health endpoint."""
    try:
        response = requests.get('http://127.0.0.1:8443/health', timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the daemon on port 8443: {e}")

    assert response.status_code == 200, f"Expected status 200 for /health, got {response.status_code}"
    assert response.text.strip() == "OK", f"Expected body 'OK' for /health, got {response.text}"

def test_daemon_lookup_missing_auth():
    """Test the /lookup endpoint without an auth token."""
    try:
        response = requests.get('http://127.0.0.1:8443/lookup?service=app2', timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the daemon on port 8443: {e}")

    assert response.status_code == 403, f"Expected status 403 for missing auth, got {response.status_code}"

def test_daemon_lookup_correct_auth():
    """Test the /lookup endpoint with the correct auth token."""
    headers = {'X-Auth-Token': 'super-secret-77X'}
    try:
        response = requests.get('http://127.0.0.1:8443/lookup?service=app2', headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the daemon on port 8443: {e}")

    assert response.status_code == 200, f"Expected status 200 for correct auth, got {response.status_code}"
    assert "192.168.1.11" in response.text, f"Expected IP '192.168.1.11' in response, got {response.text}"

def test_daemon_lookup_unknown_service():
    """Test the /lookup endpoint with an unknown service."""
    headers = {'X-Auth-Token': 'super-secret-77X'}
    try:
        response = requests.get('http://127.0.0.1:8443/lookup?service=unknown', headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the daemon on port 8443: {e}")

    assert response.status_code == 404, f"Expected status 404 for unknown service, got {response.status_code}"

def test_monitor_script():
    """Verify that the monitor.sh script exists and runs successfully."""
    monitor_path = '/home/user/monitor.sh'
    assert os.path.isfile(monitor_path), f"The monitor script {monitor_path} is missing."
    assert os.access(monitor_path, os.X_OK), f"The monitor script {monitor_path} is not executable."

    result = subprocess.run(['bash', monitor_path], capture_output=True)
    assert result.returncode == 0, f"Monitor script failed with exit code {result.returncode}. stderr: {result.stderr.decode()}"