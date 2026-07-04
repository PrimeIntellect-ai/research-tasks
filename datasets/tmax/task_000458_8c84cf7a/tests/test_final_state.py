# test_final_state.py

import os
import socket
import pytest
import requests

MALICIOUS_URL = "http://malicious.corp.attacker.local/auth_bypass"
SSH_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIObXy6kR3/58P9zB1A/N+Qz5e7J5h2W6X8Y9rVp+aE9q attacker@evil.local"

def test_deployment_log():
    """Verify the deployment.log file contains the correct extracted data."""
    log_path = "/home/user/deployment.log"
    assert os.path.exists(log_path), f"Log file not found at {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) >= 2, "deployment.log must contain at least two lines"
    assert lines[0] == MALICIOUS_URL, f"Line 1 mismatch. Expected {MALICIOUS_URL}, got {lines[0]}"
    assert lines[1] == SSH_KEY, f"Line 2 mismatch. Expected {SSH_KEY}, got {lines[1]}"

def test_http_gateway_malicious_url():
    """Verify the HTTP gateway blocks the malicious URL."""
    url = f"http://127.0.0.1:8080/redirect?target={MALICIOUS_URL}"
    try:
        response = requests.get(url, timeout=2, allow_redirects=False)
        assert response.status_code == 403, f"Expected 403 Forbidden for malicious URL, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP Gateway connection failed: {e}")

def test_http_gateway_relative_url():
    """Verify the HTTP gateway redirects relative URLs."""
    url = "http://127.0.0.1:8080/redirect?target=/settings"
    try:
        response = requests.get(url, timeout=2, allow_redirects=False)
        assert response.status_code == 302, f"Expected 302 Found for relative URL, got {response.status_code}"
        assert response.headers.get("Location") == "/settings", f"Expected Location header '/settings', got {response.headers.get('Location')}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP Gateway connection failed: {e}")

def test_http_gateway_external_url():
    """Verify the HTTP gateway blocks other external URLs."""
    url = "http://127.0.0.1:8080/redirect?target=http://google.com"
    try:
        response = requests.get(url, timeout=2, allow_redirects=False)
        assert response.status_code == 403, f"Expected 403 Forbidden for external URL, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP Gateway connection failed: {e}")

def test_ssh_service_running():
    """Verify that a service is listening on 127.0.0.1:2222 (SSH)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        result = s.connect_ex(('127.0.0.1', 2222))
        assert result == 0, "SSH service is not listening on 127.0.0.1:2222"
    finally:
        s.close()