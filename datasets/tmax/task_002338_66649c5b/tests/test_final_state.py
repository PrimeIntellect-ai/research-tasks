# test_final_state.py

import pytest
import requests
import socket
import struct
import time

def test_http_gateway():
    """Verify the HTTP Gateway correctly processes requests and responds quickly."""
    url = "http://127.0.0.1:8080/compute?val=1000"
    start_time = time.time()
    try:
        response = requests.get(url, timeout=2.0)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP Gateway request failed or timed out: {e}")

    elapsed = time.time() - start_time
    assert elapsed < 0.2, f"HTTP Gateway is too slow ({elapsed:.3f}s). The performance bug might not be fixed."

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "result" in data, f"Response JSON missing 'result' key. Got: {data}"
    assert data["result"] == 57429, f"Expected result 57429 (1000^2 % 104729), got {data['result']}"

def test_tcp_backend():
    """Verify the raw TCP Backend conforms to the binary protocol and responds quickly."""
    start_time = time.time()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(('127.0.0.1', 9090))

        # Send 32 as an 8-byte little-endian integer
        req_data = struct.pack('<q', 32)
        s.sendall(req_data)

        # Read exactly 8 bytes
        resp_data = b''
        while len(resp_data) < 8:
            chunk = s.recv(8 - len(resp_data))
            if not chunk:
                break
            resp_data += chunk

        s.close()
    except Exception as e:
        pytest.fail(f"TCP Backend request failed or timed out: {e}")

    elapsed = time.time() - start_time
    assert elapsed < 0.2, f"TCP Backend is too slow ({elapsed:.3f}s). The performance bug might not be fixed."

    assert len(resp_data) == 8, f"Expected 8 bytes from backend, got {len(resp_data)} bytes: {resp_data!r}"

    result = struct.unpack('<q', resp_data)[0]
    assert result == 1024, f"Expected result 1024 (32^2 % 104729), got {result}"