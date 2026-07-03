# test_final_state.py

import os
import socket
import requests
import pytest
import time

def djb2_hash(key: str) -> int:
    hash_val = 5381
    for char in key:
        hash_val = ((hash_val << 5) + hash_val) + ord(char)
        hash_val &= 0xFFFFFFFF
    return hash_val

def test_libhasher_compiled():
    assert os.path.isfile('/app/c_lib/libhasher.so'), "The C library was not compiled to /app/c_lib/libhasher.so"

def test_proxy_missing_api_key():
    url = "http://127.0.0.1:8080/test"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Python proxy on 127.0.0.1:8080: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized when missing X-API-Key, got {response.status_code}"

def test_proxy_rate_limiting_and_admin_flush():
    url = "http://127.0.0.1:8080/test"
    api_key = "testkey123"
    headers = {"X-API-Key": api_key}

    # 1. Send 5 requests rapidly, expect 200 OK
    for i in range(5):
        try:
            response = requests.get(url, headers=headers, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to Python proxy on request {i+1}: {e}")

        assert response.status_code == 200, f"Expected 200 OK on request {i+1}, got {response.status_code}"
        assert "API_SUCCESS" in response.text, f"Expected 'API_SUCCESS' in response body on request {i+1}, got {response.text}"

    # 2. Send 6th request, expect 429 Too Many Requests
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Python proxy on 6th request: {e}")

    assert response.status_code == 429, f"Expected 429 Too Many Requests on 6th request, got {response.status_code}"

    # 3. Calculate hash
    hashed_key = djb2_hash(api_key)

    # 4. Connect to Admin TCP protocol and flush
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(('127.0.0.1', 9000))
        s.sendall(f"FLUSH {hashed_key}\n".encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to communicate with Admin TCP protocol on 127.0.0.1:9000: {e}")

    assert data.strip() == "OK", f"Expected 'OK' from Admin TCP protocol, got '{data.strip()}'"

    # 5. Send 7th request, expect 200 OK since limit was flushed
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Python proxy after flush: {e}")

    assert response.status_code == 200, f"Expected 200 OK after flush, got {response.status_code}"
    assert "API_SUCCESS" in response.text, f"Expected 'API_SUCCESS' in response body after flush, got {response.text}"