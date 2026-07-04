# test_final_state.py
import os
import stat
import subprocess
import pytest
import requests
import urllib3

# Suppress insecure request warnings since we are using self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://127.0.0.1:8443"

def test_key_permissions():
    """Verify that the private key exists and has exactly 600 permissions."""
    key_path = "/app/certs/server.key"
    assert os.path.exists(key_path), f"Private key not found at {key_path}"

    st = os.stat(key_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o600, f"Expected permissions 600 for {key_path}, got {oct(permissions)}"

def test_certificate_subject():
    """Verify that the certificate exists and has CN=localhost."""
    cert_path = "/app/certs/server.crt"
    assert os.path.exists(cert_path), f"Certificate not found at {cert_path}"

    result = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-noout", "-subject"], 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, "Failed to read certificate subject using openssl."
    assert "CN = localhost" in result.stdout or "CN=localhost" in result.stdout, \
        f"Expected CN=localhost in certificate subject, got: {result.stdout}"

def test_server_pid_file():
    """Verify that the server PID file exists and contains a valid PID."""
    pid_path = "/app/server.pid"
    assert os.path.exists(pid_path), f"PID file not found at {pid_path}"
    with open(pid_path, "r") as f:
        pid_str = f.read().strip()
    assert pid_str.isdigit(), f"PID file contains invalid PID: {pid_str}"

def test_valid_redirect():
    """Test that a valid relative path returns a 302 Found with the correct Location header."""
    url = f"{BASE_URL}/login?next=/profile"
    try:
        response = requests.get(url, verify=False, allow_redirects=False)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 302, f"Expected 302 Found, got {response.status_code}. Response: {response.text}"
    assert response.headers.get("Location") == "/profile", \
        f"Expected Location: /profile, got {response.headers.get('Location')}"

def test_open_redirect_generic():
    """Test that an absolute URL returns a 400 Bad Request."""
    url = f"{BASE_URL}/login?next=https://google.com"
    try:
        response = requests.get(url, verify=False, allow_redirects=False)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}. Response: {response.text}"
    assert "Invalid Redirect" in response.text, \
        f"Expected 'Invalid Redirect' in response body, got: {response.text}"

def test_open_redirect_protocol_relative():
    """Test that a protocol-relative absolute URL returns a 400 Bad Request."""
    url = f"{BASE_URL}/login?next=//google.com"
    try:
        response = requests.get(url, verify=False, allow_redirects=False)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}. Response: {response.text}"
    assert "Invalid Redirect" in response.text, \
        f"Expected 'Invalid Redirect' in response body, got: {response.text}"

def test_intrusion_detection():
    """Test that the specific attacker domain returns a 403 Forbidden."""
    url = f"{BASE_URL}/login?next=http://evil-exfil-server.xyz/steal"
    try:
        response = requests.get(url, verify=False, allow_redirects=False)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {url} failed: {e}")

    assert response.status_code == 403, f"Expected 403 Forbidden, got {response.status_code}. Response: {response.text}"
    assert "Intrusion Detected" in response.text, \
        f"Expected 'Intrusion Detected' in response body, got: {response.text}"