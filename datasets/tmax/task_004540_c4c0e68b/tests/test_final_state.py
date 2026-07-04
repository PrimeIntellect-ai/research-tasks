# test_final_state.py

import os
import requests
import urllib3
import pytest

# Disable insecure request warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_files_exist():
    """Verify that the required files and directories were created."""
    assert os.path.isdir("/home/user/nginx_setup"), "/home/user/nginx_setup directory is missing"
    assert os.path.isfile("/home/user/nginx_setup/nginx.conf"), "nginx.conf is missing in /home/user/nginx_setup/"
    assert os.path.isfile("/home/user/nginx_setup/server.crt"), "TLS certificate server.crt is missing"
    assert os.path.isfile("/home/user/nginx_setup/server.key"), "TLS private key server.key is missing"
    assert os.path.isfile("/home/user/proxy_server"), "Compiled proxy_server binary is missing"

def test_normal_request_and_redaction():
    """Verify that a normal request is proxied correctly and the session_id cookie is redacted."""
    headers = {"Cookie": "session_id=abc123XYZ; theme=dark"}
    try:
        resp = requests.get("https://127.0.0.1:8443/", headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8443: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200 OK, got {resp.status_code}. Response: {resp.text}"

    # The backend echoes headers. Check if the session_id was redacted.
    assert "session_id=REDACTED" in resp.text, f"session_id cookie was not properly redacted. Response body:\n{resp.text}"
    assert "theme=dark" in resp.text, f"Other cookies were incorrectly modified or dropped. Response body:\n{resp.text}"

def test_vulnerability_scanning_prevention_union_select():
    """Verify that a request containing 'UNION SELECT' is blocked."""
    try:
        resp = requests.get("https://127.0.0.1:8443/?query=UNION SELECT * FROM users", verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8443: {e}")

    assert resp.status_code == 403, f"Expected HTTP 403 Forbidden for UNION SELECT, got {resp.status_code}. Response: {resp.text}"
    assert resp.text == "Malicious payload", f"Expected body 'Malicious payload', got {resp.text}"

def test_vulnerability_scanning_prevention_script():
    """Verify that a request containing '<script>' in the User-Agent is blocked."""
    headers = {"User-Agent": "Mozilla <script>alert(1)</script>"}
    try:
        resp = requests.post("https://127.0.0.1:8443/submit", headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8443: {e}")

    assert resp.status_code == 403, f"Expected HTTP 403 Forbidden for <script>, got {resp.status_code}. Response: {resp.text}"
    assert resp.text == "Malicious payload", f"Expected body 'Malicious payload', got {resp.text}"