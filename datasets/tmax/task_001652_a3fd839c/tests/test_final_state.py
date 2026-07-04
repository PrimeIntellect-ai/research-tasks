# test_final_state.py

import os
import stat
import pytest
import requests

EVIDENCE_DIR = "/home/user/evidence"
ATTACKER_IP_FILE = "/home/user/evidence/attacker_ip.txt"
EXPECTED_IP = "198.51.100.42"
BASE_URL = "http://127.0.0.1:8080"

def test_attacker_ip_file_content():
    """Verify that the attacker IP was correctly extracted and saved."""
    assert os.path.isfile(ATTACKER_IP_FILE), f"Evidence file not found: {ATTACKER_IP_FILE}"
    with open(ATTACKER_IP_FILE, "r") as f:
        content = f.read().strip()
    assert content == EXPECTED_IP, f"Expected IP {EXPECTED_IP}, but found {content} in {ATTACKER_IP_FILE}"

def test_evidence_permissions():
    """Verify that the evidence directory and files have correct permissions."""
    assert os.path.isdir(EVIDENCE_DIR), f"Evidence directory not found: {EVIDENCE_DIR}"

    # Check directory permissions (700)
    dir_stat = os.stat(EVIDENCE_DIR)
    assert stat.S_IMODE(dir_stat.st_mode) == 0o700, f"Evidence directory permissions are {oct(stat.S_IMODE(dir_stat.st_mode))}, expected 0o700"

    # Check file permissions (600)
    for root, dirs, files in os.walk(EVIDENCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            file_stat = os.stat(file_path)
            assert stat.S_IMODE(file_stat.st_mode) == 0o600, f"File permissions for {file_path} are {oct(stat.S_IMODE(file_stat.st_mode))}, expected 0o600"

def test_http_service_running_and_serves_evidence():
    """Verify that darkhttpd is running and serving the evidence directory."""
    url = f"{BASE_URL}/attacker_ip.txt"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for {url}, got {response.status_code}"
    assert EXPECTED_IP in response.text, f"Expected IP {EXPECTED_IP} in response body, got {response.text}"

def test_http_service_backdoor_removed():
    """Verify that the backdoor has been removed and path traversal is blocked."""
    url = f"{BASE_URL}/../../../../etc/passwd"
    headers = {"X-Attacker-Auth": "backdoor"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}: {e}")

    assert response.status_code != 200, f"Expected HTTP status code to not be 200 OK for {url} with backdoor header. The backdoor is likely still present."
    assert response.status_code in [400, 403, 404], f"Expected HTTP 400, 403, or 404 for {url}, got {response.status_code}"