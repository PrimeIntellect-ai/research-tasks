# test_final_state.py
import socket
import requests
import hashlib
import pytest

TOKEN = "SECURE_AUDIT_9982"
HTTP_URL = "http://127.0.0.1:8080"
TCP_HOST = "127.0.0.1"
TCP_PORT = 8081

CSP_HEADER_EXPECTED = "default-src 'none'; frame-ancestors 'none';"

def test_http_404_and_csp():
    """Test that a GET request to / returns 404 and includes the CSP header."""
    try:
        response = requests.get(HTTP_URL, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service on port 8080: {e}")

    assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}"
    csp = response.headers.get("Content-Security-Policy", "")
    assert csp == CSP_HEADER_EXPECTED, f"Expected CSP header '{CSP_HEADER_EXPECTED}', got '{csp}'"

def test_http_audit_no_token():
    """Test that POST /audit without a token returns 401."""
    try:
        response = requests.post(f"{HTTP_URL}/audit", data="test", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service on port 8080: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    csp = response.headers.get("Content-Security-Policy", "")
    assert csp == CSP_HEADER_EXPECTED, f"Expected CSP header '{CSP_HEADER_EXPECTED}', got '{csp}'"

def test_http_audit_with_token():
    """Test that POST /audit with the correct token returns 200 and the correct X-Body-Hash."""
    payload = "test_payload"
    expected_hash = hashlib.sha256(payload.encode()).hexdigest()
    headers = {"Authorization": f"Bearer {TOKEN}"}

    try:
        response = requests.post(f"{HTTP_URL}/audit", headers=headers, data=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service on port 8080: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    csp = response.headers.get("Content-Security-Policy", "")
    assert csp == CSP_HEADER_EXPECTED, f"Expected CSP header '{CSP_HEADER_EXPECTED}', got '{csp}'"

    body_hash = response.headers.get("X-Body-Hash", "")
    assert body_hash == expected_hash, f"Expected X-Body-Hash '{expected_hash}', got '{body_hash}'"

def test_tcp_valid_scan():
    """Test the TCP service with the correct scan command."""
    try:
        with socket.create_connection((TCP_HOST, TCP_PORT), timeout=2) as s:
            s.sendall(f"SCAN {TOKEN}\n".encode())
            data = s.recv(1024).decode()
            assert data == "VALID\n", f"Expected 'VALID\\n', got {repr(data)}"
    except socket.error as e:
        pytest.fail(f"Failed to connect or communicate with TCP service on port 8081: {e}")

def test_tcp_invalid_scan():
    """Test the TCP service with an incorrect scan command."""
    try:
        with socket.create_connection((TCP_HOST, TCP_PORT), timeout=2) as s:
            s.sendall(b"SCAN WRONG\n")
            data = s.recv(1024).decode()
            assert data == "REJECTED\n", f"Expected 'REJECTED\\n', got {repr(data)}"
    except socket.error as e:
        pytest.fail(f"Failed to connect or communicate with TCP service on port 8081: {e}")