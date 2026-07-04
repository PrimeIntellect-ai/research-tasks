# test_final_state.py

import os
import time
import base64
import ctypes
import requests
import pytest

URL = "http://127.0.0.1:9090/api/v1/release/check"
AUTH_HEADER = {"Authorization": "Bearer secr3t-d3pl0y-t0k3n"}

@pytest.fixture(scope="session", autouse=True)
def wait_for_ready():
    """Wait for the ready.txt file to be created and contain READY."""
    ready_file = "/home/user/ready.txt"
    timeout = 10
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(ready_file):
            with open(ready_file, "r") as f:
                if "READY" in f.read():
                    return
        time.sleep(0.5)
    pytest.fail(f"Service not ready: {ready_file} not found or does not contain 'READY'.")

@pytest.fixture(scope="session")
def mathcheck_lib():
    """Load the compiled shared library to compute expected parities."""
    so_path = "/app/libmathcheck-1.2.4/libmathcheck.so"
    assert os.path.exists(so_path), f"Shared library {so_path} not found. Ensure Makefile builds it."
    try:
        lib = ctypes.CDLL(so_path)
        lib.calculate_parity.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
        lib.calculate_parity.restype = ctypes.c_uint32
        return lib
    except Exception as e:
        pytest.fail(f"Failed to load {so_path}: {e}")

def get_parity(lib, data_bytes: bytes) -> int:
    return lib.calculate_parity(data_bytes, len(data_bytes))

def test_missing_auth():
    """Test that missing authorization header returns 401."""
    resp = requests.post(URL, json={})
    assert resp.status_code == 401, f"Expected 401 for missing auth, got {resp.status_code}"

def test_invalid_auth():
    """Test that invalid authorization header returns 401."""
    resp = requests.post(URL, headers={"Authorization": "Bearer wrong-token"}, json={})
    assert resp.status_code == 401, f"Expected 401 for invalid auth, got {resp.status_code}"

def test_version_upgrade_required():
    """Test that version < 2.0.0-rc.1 returns 426."""
    payload = {
        "version": "1.9.9",
        "payload": "SGVsbG8=",
        "expected_parity": 0
    }
    resp = requests.post(URL, headers=AUTH_HEADER, json=payload)
    assert resp.status_code == 426, f"Expected 426 for old version, got {resp.status_code}"

def test_valid_request_short_payload(mathcheck_lib):
    """Test a valid request with a short payload."""
    data = b"Hello World\n"
    b64_data = base64.b64encode(data).decode('utf-8')
    parity = get_parity(mathcheck_lib, data)

    payload = {
        "version": "2.0.0",
        "payload": b64_data,
        "expected_parity": parity
    }
    resp = requests.post(URL, headers=AUTH_HEADER, json=payload)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    assert resp.json().get("status") == "ok", "Expected status: ok in response"

def test_valid_request_long_payload(mathcheck_lib):
    """Test a valid request with a payload > 16 bytes to ensure UB is fixed."""
    data = b"A very long string that is greater than 16 bytes to trigger UB"
    b64_data = base64.b64encode(data).decode('utf-8')
    parity = get_parity(mathcheck_lib, data)

    payload = {
        "version": "2.1.0",
        "payload": b64_data,
        "expected_parity": parity
    }
    resp = requests.post(URL, headers=AUTH_HEADER, json=payload)
    assert resp.status_code == 200, f"Expected 200 OK for long payload, got {resp.status_code}. Response: {resp.text}"
    assert resp.json().get("status") == "ok", "Expected status: ok in response"

def test_wrong_parity(mathcheck_lib):
    """Test that an incorrect parity returns 400."""
    data = b"Some payload"
    b64_data = base64.b64encode(data).decode('utf-8')
    parity = get_parity(mathcheck_lib, data)

    payload = {
        "version": "2.0.0",
        "payload": b64_data,
        "expected_parity": parity + 1  # Intentionally wrong
    }
    resp = requests.post(URL, headers=AUTH_HEADER, json=payload)
    assert resp.status_code == 400, f"Expected 400 for wrong parity, got {resp.status_code}. Response: {resp.text}"
    assert resp.json().get("status") == "mismatch", "Expected status: mismatch in response"

def test_invalid_json():
    """Test that malformed JSON returns 400."""
    resp = requests.post(URL, headers=AUTH_HEADER, data="not a json")
    assert resp.status_code == 400, f"Expected 400 for invalid JSON, got {resp.status_code}"

def test_invalid_base64():
    """Test that invalid base64 payload returns 400."""
    payload = {
        "version": "2.0.0",
        "payload": "not-valid-base64!@#",
        "expected_parity": 0
    }
    resp = requests.post(URL, headers=AUTH_HEADER, json=payload)
    assert resp.status_code == 400, f"Expected 400 for invalid base64, got {resp.status_code}"