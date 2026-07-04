# test_final_state.py

import math
import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090/api/v1/calculate"
HEADERS = {"Authorization": "Bearer secret-math-key"}

def test_auth_missing():
    """Test that missing Authorization header results in 401."""
    resp = requests.post(BASE_URL, json={"price": 100, "vol": 0.5, "time": 1.0})
    assert resp.status_code == 401, f"Expected 401 for missing auth, got {resp.status_code}"

def test_auth_wrong():
    """Test that incorrect Authorization header results in 401."""
    resp = requests.post(BASE_URL, headers={"Authorization": "Bearer wrong-key"}, json={"price": 100, "vol": 0.5, "time": 1.0})
    assert resp.status_code == 401, f"Expected 401 for wrong auth, got {resp.status_code}"

def test_payload_missing():
    """Test that an empty JSON payload results in 400."""
    resp = requests.post(BASE_URL, headers=HEADERS, json={})
    assert resp.status_code == 400, f"Expected 400 for empty payload, got {resp.status_code}"

def test_payload_bad_json():
    """Test that malformed JSON results in 400."""
    resp = requests.post(BASE_URL, headers=HEADERS, data="not json")
    assert resp.status_code == 400, f"Expected 400 for bad JSON, got {resp.status_code}"

def test_validation_price_high():
    """Test that price > 10000 results in 400."""
    resp = requests.post(BASE_URL, headers=HEADERS, json={"price": 10001, "vol": 0.5, "time": 1.0})
    assert resp.status_code == 400, f"Expected 400 for price > 10000, got {resp.status_code}"

def test_validation_vol_low():
    """Test that vol <= 0 results in 400."""
    resp = requests.post(BASE_URL, headers=HEADERS, json={"price": 100, "vol": -0.1, "time": 1.0})
    assert resp.status_code == 400, f"Expected 400 for vol <= 0, got {resp.status_code}"

def test_validation_time_low():
    """Test that time < 0.1 results in 400."""
    resp = requests.post(BASE_URL, headers=HEADERS, json={"price": 100, "vol": 0.5, "time": 0.05})
    assert resp.status_code == 400, f"Expected 400 for time < 0.1, got {resp.status_code}"

def test_valid_request():
    """Test a valid request returns 200 and the correct mathematical result."""
    time.sleep(1.1)  # Ensure rate limits are reset
    price, vol, t = 100.0, 0.5, 1.0
    resp = requests.post(BASE_URL, headers=HEADERS, json={"price": price, "vol": vol, "time": t})
    assert resp.status_code == 200, f"Expected 200 for valid request, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response was not valid JSON: {resp.text}")

    assert "result" in data, "Response JSON missing 'result' key"

    expected = price * math.exp(vol * math.sqrt(t))
    assert math.isclose(data["result"], expected, rel_tol=1e-4), f"Expected result ~{expected}, got {data['result']}"

def test_rate_limiting():
    """Test that the rate limiter blocks the 4th request within a second."""
    time.sleep(1.5)  # Wait for rate limiter to fully reset

    payload = {"price": 100, "vol": 0.5, "time": 1.0}

    # Send 3 valid requests, they should all succeed
    for i in range(3):
        resp = requests.post(BASE_URL, headers=HEADERS, json=payload)
        assert resp.status_code == 200, f"Request {i+1}/3 failed with {resp.status_code}, expected 200"

    # The 4th request should be rate limited
    resp4 = requests.post(BASE_URL, headers=HEADERS, json=payload)
    assert resp4.status_code == 429, f"Expected 429 for 4th request, got {resp4.status_code}"