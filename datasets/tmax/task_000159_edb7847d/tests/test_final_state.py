# test_final_state.py

import os
import requests
import pytest
import urllib3

# Suppress insecure request warnings for the self-signed/dummy cert
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HTTP_URL = "http://127.0.0.1:8080/callback"
HTTPS_URL = "https://127.0.0.1:8443/callback"
EXPECTED_COOKIE = "c2_session=v9x8b7a6m5n4"
ACCESS_LOG_PATH = "/home/user/access.log"
PEM_PATH = "/home/user/server.pem"

def test_http_valid_auth():
    """
    Test that the HTTP listener on port 8080 responds correctly to a valid authentication cookie.
    """
    headers = {
        "Cookie": EXPECTED_COOKIE,
        "User-Agent": "C2-Probe/1.0"
    }

    try:
        response = requests.get(HTTP_URL, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Failed to connect to HTTP server at {HTTP_URL}. Is the server running?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {HTTP_URL} timed out.")

    assert response.status_code == 200, f"Expected HTTP 200 OK for valid auth, got {response.status_code}. Response body: {response.text}"
    assert response.text.strip() == "ACK_AUTH_VALID", f"Expected body 'ACK_AUTH_VALID', got '{response.text}'"

def test_https_invalid_auth():
    """
    Test that the HTTPS listener on port 8443 responds correctly to an invalid authentication cookie.
    """
    headers = {
        "Cookie": "c2_session=invalid",
        "User-Agent": "C2-Probe/2.0"
    }

    try:
        # verify=False because the certificate is likely self-signed or a dummy
        response = requests.get(HTTPS_URL, headers=headers, verify=False, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Failed to connect to HTTPS server at {HTTPS_URL}. Is the server running and bound to the correct port?")
    except requests.exceptions.SSLError as e:
        pytest.fail(f"SSL error connecting to {HTTPS_URL}. Did you configure the TLS context correctly? Error: {e}")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {HTTPS_URL} timed out.")

    assert response.status_code == 403, f"Expected HTTP 403 Forbidden for invalid auth, got {response.status_code}. Response body: {response.text}"
    assert response.text.strip() == "ERR_UNAUTHORIZED", f"Expected body 'ERR_UNAUTHORIZED', got '{response.text}'"

def test_access_log_contains_valid_user_agent():
    """
    Test that the access log was created and contains the User-Agent of the valid request.
    """
    assert os.path.exists(ACCESS_LOG_PATH), f"Access log file not found at {ACCESS_LOG_PATH}"

    with open(ACCESS_LOG_PATH, "r") as f:
        log_contents = f.read()

    assert "C2-Probe/1.0" in log_contents, f"Expected 'C2-Probe/1.0' in {ACCESS_LOG_PATH}, but it was not found. Contents: {log_contents}"

def test_pem_file_exists():
    """
    Test that the recovered PEM certificate was saved to the correct location.
    """
    assert os.path.exists(PEM_PATH), f"Recovered certificate file not found at {PEM_PATH}"

    with open(PEM_PATH, "r") as f:
        content = f.read()
        assert "-----BEGIN CERTIFICATE-----" in content, f"File at {PEM_PATH} does not appear to contain a valid PEM certificate."