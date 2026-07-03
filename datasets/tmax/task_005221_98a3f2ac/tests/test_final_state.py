# test_final_state.py

import os
import time
import socket
import subprocess
import requests
import pytest

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def test_scripts_exist():
    """Ensure the required scripts exist and are executable."""
    scripts = [
        "/home/user/monitor.py",
        "/home/user/manage.sh",
        "/home/user/deploy.sh"
    ]
    for script in scripts:
        assert os.path.exists(script), f"Script {script} does not exist"
        assert os.access(script, os.X_OK) or script.endswith('.py'), f"Script {script} is not executable"

def test_health_endpoint():
    """Test that the /health endpoint returns 200 OK and correct JSON."""
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /health endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /health is not valid JSON")

    assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"

def test_alerts_endpoint():
    """Test that the /alerts endpoint returns the correct black frames."""
    try:
        response = requests.get("http://127.0.0.1:8080/alerts", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /alerts endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /alerts is not valid JSON")

    assert "black_frames" in data, "Response JSON missing 'black_frames' key"
    frames = data["black_frames"]
    assert isinstance(frames, list), "'black_frames' should be a list"
    assert sorted(frames) == [3, 8], f"Expected black frames [3, 8], got {frames}"

def test_manage_sh_lifecycle():
    """Test manage.sh status and stop functionality."""
    manage_script = "/home/user/manage.sh"

    # Test status
    status_proc = subprocess.run([manage_script, "status"], capture_output=True)
    assert status_proc.returncode == 0, f"manage.sh status returned non-zero exit code: {status_proc.returncode}"

    # Test stop
    stop_proc = subprocess.run([manage_script, "stop"], capture_output=True)
    assert stop_proc.returncode == 0, f"manage.sh stop returned non-zero exit code: {stop_proc.returncode}"

    # Give it a moment to shut down
    time.sleep(1)

    # Verify port is unbound
    assert not is_port_open(8080), "Port 8080 is still bound after running manage.sh stop"