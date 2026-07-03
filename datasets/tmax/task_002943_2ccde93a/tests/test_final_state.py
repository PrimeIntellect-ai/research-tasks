# test_final_state.py

import os
import time
import requests
import pytest

def test_shared_library_exists():
    assert os.path.isfile("/app/pow_shield/libpow_shield.so"), "Shared library libpow_shield.so was not built in /app/pow_shield/"

def test_proxy_valid_pow():
    # Sleep to ensure the EMA rate limiter does not trigger (EMA stays high)
    time.sleep(0.5)

    payload = {"data": "test", "nonce": 4, "target": 10}
    try:
        resp = requests.post("http://127.0.0.1:8000/submit", json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the proxy server: {e}")

    assert resp.status_code == 200, f"Expected 200 OK for valid PoW, got {resp.status_code}: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert data.get("status") == "Accepted", f"Expected JSON {{'status': 'Accepted'}}, got {data}"

def test_proxy_invalid_pow():
    # Sleep to ensure the EMA rate limiter does not trigger
    time.sleep(0.5)

    payload = {"data": "test", "nonce": 5, "target": 10}
    try:
        resp = requests.post("http://127.0.0.1:8000/submit", json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the proxy server: {e}")

    assert resp.status_code == 403, f"Expected 403 Forbidden for invalid PoW, got {resp.status_code}: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert data.get("error") == "Invalid PoW", f"Expected JSON {{'error': 'Invalid PoW'}}, got {data}"

def test_proxy_rate_limiting():
    # Send requests rapidly to trigger the EMA rate limit
    # EMA formula: EMA = (diff_ms * 0.3) + (previous_EMA * 0.7)
    # With diff_ms ~ 0, EMA will decay by 0.7 each time.
    # Starting from ~500, it should take around 5-6 requests to drop below 100.0

    rate_limited = False
    payload = {"data": "test", "nonce": 4, "target": 10}

    for _ in range(15):
        try:
            resp = requests.post("http://127.0.0.1:8000/submit", json=payload, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to the proxy server during rate limit test: {e}")

        if resp.status_code == 429:
            rate_limited = True
            try:
                data = resp.json()
            except ValueError:
                pytest.fail(f"Response is not valid JSON: {resp.text}")

            assert data.get("error") == "Too Fast", f"Expected JSON {{'error': 'Too Fast'}}, got {data}"
            break

    assert rate_limited, "Expected rate limit (HTTP 429) to trigger after rapid consecutive requests, but it did not."