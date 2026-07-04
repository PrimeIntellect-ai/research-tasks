# test_final_state.py

import os
import re
import socket
import requests
import pytest

def test_bashrc_contains_token():
    """Verify that the required environment variable is set in .bashrc."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.exists(bashrc_path), f"File not found: {bashrc_path}"

    with open(bashrc_path, "r") as f:
        content = f.read()

    # Check for the token discovered from the binary
    assert "STORAGE_AUTH_TOKEN" in content, "STORAGE_AUTH_TOKEN not found in .bashrc"
    assert "7x9_MONITOR_KEY_x99" in content, "Correct token value not found in .bashrc"

def test_http_status_endpoint():
    """Verify that the HTTP proxy /status endpoint returns 'UP'."""
    try:
        response = requests.get("http://127.0.0.1:8080/status", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP proxy on port 8080: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.text.strip() == "UP", f"Expected response 'UP', got '{response.text}'"

def test_http_metrics_endpoint():
    """Verify that the HTTP proxy /metrics endpoint returns Prometheus formatted metrics."""
    try:
        response = requests.get("http://127.0.0.1:8080/metrics", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP proxy on port 8080: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    text = response.text.strip()

    used_match = re.search(r"^storage_disk_used_mb\s+(\d+(?:\.\d+)?)$", text, re.MULTILINE)
    quota_match = re.search(r"^storage_disk_quota_mb\s+(\d+(?:\.\d+)?)$", text, re.MULTILINE)

    assert used_match is not None, f"Could not find 'storage_disk_used_mb <value>' in response:\n{text}"
    assert quota_match is not None, f"Could not find 'storage_disk_quota_mb <value>' in response:\n{text}"

def test_tcp_alert_socket():
    """Verify that the TCP alert socket responds correctly to 'CHECK\\n'."""
    try:
        with socket.create_connection(("127.0.0.1", 8081), timeout=5) as sock:
            sock.sendall(b"CHECK\n")
            data = sock.recv(1024).decode("utf-8")
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with TCP alert socket on port 8081: {e}")

    assert data in ["OK\n", "ALERT\n"], f"Expected 'OK\\n' or 'ALERT\\n', got {repr(data)}"

    # Based on the mocked daemon returning 460/500 (92%), it should be ALERT
    assert data == "ALERT\n", f"Expected 'ALERT\\n' since 460/500 > 90%, got {repr(data)}"