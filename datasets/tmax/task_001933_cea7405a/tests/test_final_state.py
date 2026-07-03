# test_final_state.py

import os
import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090/api/v1/compute"
AUTH_HEADER = {"Authorization": "Bearer secret-QA-8821"}

def encode_expr(expr: str) -> str:
    """Helper to encode math expressions according to the legacy binary logic."""
    return "".join(f"{ord(c) ^ 0x5A:02x}" for c in expr)

def test_ci_script_exists():
    """Verify the CI test script exists and is executable."""
    path = "/home/user/ci_test.sh"
    assert os.path.isfile(path), f"Missing {path}"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_unauthorized():
    """Verify that requests without proper authentication are rejected with 401."""
    time.sleep(10.1)  # Ensure rate limit window is clear
    resp = requests.post(BASE_URL, json={"data": encode_expr("1+1")})
    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}. Response: {resp.text}"

def test_bad_request():
    """Verify that malformed requests are rejected with 400."""
    time.sleep(10.1)  # Ensure rate limit window is clear

    # Missing 'data' key
    resp1 = requests.post(BASE_URL, headers=AUTH_HEADER, json={"wrong_key": encode_expr("1+1")})
    assert resp1.status_code == 400, f"Expected 400 Bad Request for missing 'data' key, got {resp1.status_code}. Response: {resp1.text}"

    # Non-hex string
    resp2 = requests.post(BASE_URL, headers=AUTH_HEADER, json={"data": "not-a-valid-hex-string"})
    assert resp2.status_code == 400, f"Expected 400 Bad Request for non-hex data, got {resp2.status_code}. Response: {resp2.text}"

def test_valid_computation():
    """Verify that the mock server correctly decodes and computes the result."""
    time.sleep(10.1)  # Ensure rate limit window is clear

    expr = "15*3"
    payload = {"data": encode_expr(expr)}
    resp = requests.post(BASE_URL, headers=AUTH_HEADER, json=payload)

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "result" in data, f"Response JSON missing 'result' key. Got: {data}"
    assert data["result"] == 45, f"Expected result 45 for '15*3', got {data['result']}"

def test_rate_limiting():
    """Verify that the rate limit of 3 requests per 10 seconds is enforced."""
    time.sleep(10.1)  # Ensure rate limit window is clear

    expr = "2+2"
    payload = {"data": encode_expr(expr)}

    # First 3 requests should succeed
    for i in range(3):
        resp = requests.post(BASE_URL, headers=AUTH_HEADER, json=payload)
        assert resp.status_code == 200, f"Request {i+1}/3 failed with {resp.status_code}, expected 200. Response: {resp.text}"

    # 4th request should be rate limited
    resp_429 = requests.post(BASE_URL, headers=AUTH_HEADER, json=payload)
    assert resp_429.status_code == 429, f"Expected 429 Too Many Requests for 4th request, got {resp_429.status_code}. Response: {resp_429.text}"