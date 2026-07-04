# test_final_state.py

import socket
import pytest

HOST = '127.0.0.1'
PORT = 8080
TIMEOUT = 2.0

def send_request(request_str: str) -> str:
    """Helper to send a request to the auth service and read the response."""
    try:
        with socket.create_connection((HOST, PORT), timeout=TIMEOUT) as s:
            s.sendall(request_str.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response
    except ConnectionRefusedError:
        pytest.fail(f"Connection refused to {HOST}:{PORT}. Is the service running?")
    except socket.timeout:
        pytest.fail(f"Connection to {HOST}:{PORT} timed out waiting for response.")
    except Exception as e:
        pytest.fail(f"Unexpected error communicating with service: {e}")

def test_valid_user_request():
    """Test a valid user request."""
    request = "AUTH v1 alice cd1af472d5045479ec364377bb411bc7 68656c6c6f\n"
    expected = "ACCEPT: USER\n"
    response = send_request(request)
    assert response == expected, f"Expected {expected!r}, got {response!r}"

def test_valid_admin_request():
    """Test a valid admin request."""
    request = "AUTH v1 bob ea7223b24660eb0e94bb510bbf819340 737570657261646d696e313233\n"
    expected = "ACCEPT: ADMIN\n"
    response = send_request(request)
    assert response == expected, f"Expected {expected!r}, got {response!r}"

def test_intrusion_attempt_valid_hash():
    """Test an intrusion attempt with a valid hash (should be rejected as intrusion)."""
    request = "AUTH v1 al'ice cd1af472d5045479ec364377bb411bc7 68656c6c6f\n"
    expected = "REJECT: INTRUSION\n"
    response = send_request(request)
    assert response == expected, f"Expected {expected!r}, got {response!r}"

def test_intrusion_attempt_invalid_hash():
    """Test an intrusion attempt with an invalid hash (intrusion check must happen first)."""
    request = "AUTH v1 admin; 00000000000000000000000000000000 68656c6c6f\n"
    expected = "REJECT: INTRUSION\n"
    response = send_request(request)
    assert response == expected, f"Expected {expected!r}, got {response!r}"

def test_integrity_failure():
    """Test an integrity failure (bad hash, clean username)."""
    request = "AUTH v1 charlie 11111111111111111111111111111111 68656c6c6f\n"
    expected = "REJECT: INTEGRITY\n"
    response = send_request(request)
    assert response == expected, f"Expected {expected!r}, got {response!r}"