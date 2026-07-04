# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
ENDPOINT = f"{BASE_URL}/api/v1/upload"
EXPECTED_AUTH_HEADER = "admin456:10.99.5.42"
EXPECTED_CSP = "default-src 'self'; script-src 'none';"

def check_csp_header(response):
    csp = response.headers.get("Content-Security-Policy")
    assert csp is not None, "Content-Security-Policy header is missing from the response."
    assert csp == EXPECTED_CSP, f"Content-Security-Policy header is incorrect. Expected: {EXPECTED_CSP}, Got: {csp}"

def test_missing_auth():
    """Test that missing X-Incident-Auth header returns 401 Unauthorized."""
    try:
        response = requests.post(ENDPOINT, json={"filename": "safe.txt"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {ENDPOINT}: {e}")

    assert response.status_code == 401, f"Expected 401 for missing auth, got {response.status_code}. Response: {response.text}"
    check_csp_header(response)

def test_incorrect_auth():
    """Test that incorrect X-Incident-Auth header returns 401 Unauthorized."""
    headers = {"X-Incident-Auth": "wrongpassword:10.99.5.42"}
    try:
        response = requests.post(ENDPOINT, headers=headers, json={"filename": "safe.txt"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {ENDPOINT}: {e}")

    assert response.status_code == 401, f"Expected 401 for incorrect auth, got {response.status_code}. Response: {response.text}"
    check_csp_header(response)

def test_path_traversal_forward_slash():
    """Test that a filename containing '../' returns 400 Bad Request."""
    headers = {"X-Incident-Auth": EXPECTED_AUTH_HEADER}
    payload = {"filename": "../../../etc/passwd"}
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {ENDPOINT}: {e}")

    assert response.status_code == 400, f"Expected 400 for path traversal '../', got {response.status_code}. Response: {response.text}"
    check_csp_header(response)

def test_path_traversal_backslash():
    """Test that a filename containing '..\\' returns 400 Bad Request."""
    headers = {"X-Incident-Auth": EXPECTED_AUTH_HEADER}
    payload = {"filename": "..\\..\\..\\windows\\system32"}
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {ENDPOINT}: {e}")

    assert response.status_code == 400, f"Expected 400 for path traversal '..\\', got {response.status_code}. Response: {response.text}"
    check_csp_header(response)

def test_successful_upload():
    """Test that a safe filename returns 200 OK."""
    headers = {"X-Incident-Auth": EXPECTED_AUTH_HEADER}
    payload = {"filename": "report.pdf"}
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {ENDPOINT}: {e}")

    assert response.status_code == 200, f"Expected 200 for safe filename, got {response.status_code}. Response: {response.text}"
    check_csp_header(response)