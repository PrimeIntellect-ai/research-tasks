# test_final_state.py

import os
import requests
import urllib3
import pytest

# Suppress insecure request warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://127.0.0.1:8443/audit-report"
AUTH_TOKEN = "SecT0k3n_99xA"
REDACT_USER = "admin_charlie"

def test_certs_exist():
    """Test that the certificate and key files exist in the required directory."""
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing."
    assert os.path.isfile(key_path), f"Private key file {key_path} is missing."

def test_unauthenticated_request():
    """Test that a request without the correct Authorization header returns 401."""
    try:
        response = requests.get(URL, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for unauthenticated request, got {response.status_code}."

def test_authenticated_request_and_redaction():
    """Test that a request with the correct Authorization header returns 200, correct headers, and redacted body."""
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }

    try:
        response = requests.get(URL, headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for authenticated request, got {response.status_code}."

    # Check Content-Security-Policy header
    csp_header = response.headers.get("Content-Security-Policy")
    expected_csp = "default-src 'self'; frame-ancestors 'none';"
    assert csp_header == expected_csp, f"Expected CSP header '{expected_csp}', got '{csp_header}'."

    # Check body for redaction
    body = response.text
    assert REDACT_USER not in body, f"Found unredacted username '{REDACT_USER}' in the response body."
    assert "[REDACTED]" in body, "Expected to find '[REDACTED]' in the response body."

    # Check that other content is still present
    assert "user_alice" in body, "Expected content 'user_alice' missing from the response body."
    assert "LOGIN SUCCESS" in body, "Expected content 'LOGIN SUCCESS' missing from the response body."