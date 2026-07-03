# test_final_state.py

import socket
import json
import requests
import pytest

def get_expected_signature():
    # Derive the expected signature dynamically based on the algorithm
    # Payload: b'\xFF\xFF\xFF\xFF\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'
    # Unpacked as '<IIII': 4294967295, 1, 2, 3
    seed = 1
    vals = [4294967295, 1, 2, 3]
    for v in vals:
        seed = (seed * v) & 0xFFFFFFFFFFFFFFFF

    while seed % 10007 != 0:
        seed = (seed * 1337 + 1) & 0xFFFFFFFFFFFFFFFF
    return str(seed)

PAYLOAD = b'\xFF\xFF\xFF\xFF\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'

def test_backend_tcp_service():
    """Verify the backend crypto node directly on port 8081."""
    expected_sig = get_expected_signature().encode()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3.0)
        s.connect(('127.0.0.1', 8081))
        s.sendall(PAYLOAD)
        res = s.recv(1024)
        s.close()
    except ConnectionRefusedError:
        pytest.fail("Backend crypto node is not listening on 127.0.0.1:8081")
    except socket.timeout:
        pytest.fail("Backend crypto node timed out. The signed integer bug might still exist.")

    assert res != b"ERROR", "Backend returned ERROR. The unpacking logic might still be failing."
    assert res == expected_sig, f"Backend returned incorrect signature: {res} (expected {expected_sig})"

def test_frontend_http_service():
    """Verify the frontend gateway on port 8080."""
    expected_sig = get_expected_signature()

    try:
        response = requests.post(
            'http://127.0.0.1:8080/analyze',
            data=PAYLOAD,
            timeout=3.0
        )
    except requests.exceptions.ConnectionError:
        pytest.fail("Frontend gateway is not listening on 127.0.0.1:8080")
    except requests.exceptions.Timeout:
        pytest.fail("Frontend gateway timed out. It might be misconfigured or blocked.")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. The gateway port bug might still exist."

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Gateway did not return valid JSON. Response body: {response.text}")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("signature") == expected_sig, f"Gateway returned incorrect signature: {data.get('signature')} (expected {expected_sig})"