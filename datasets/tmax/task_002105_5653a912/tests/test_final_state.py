# test_final_state.py

import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"

def get_goroutines():
    try:
        response = requests.get(f"{BASE_URL}/goroutines", timeout=2)
        response.raise_for_status()
        return int(response.text.strip())
    except Exception as e:
        pytest.fail(f"Failed to fetch goroutines count: {e}")

def test_service_fixes():
    # 1. Ensure the service is up and get baseline goroutines
    baseline_goroutines = get_goroutines()

    # 2. Test valid JSON request
    try:
        resp = requests.post(f"{BASE_URL}/process", json={"data": "test"}, timeout=2)
        assert resp.status_code == 200, f"Expected HTTP 200 for valid JSON, got {resp.status_code}"
        assert resp.text == "processed", f"Expected 'processed' response, got '{resp.text}'"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Valid request failed: {e}")

    # 3. Test corrupted JSON request
    try:
        # Sending raw string that is malformed JSON
        resp = requests.post(f"{BASE_URL}/process", data='{"data": "test"', timeout=2)
        assert resp.status_code == 400, f"Expected HTTP 400 for corrupted JSON, got {resp.status_code}"
    except requests.exceptions.Timeout:
        pytest.fail("Service hung on corrupted JSON input (timeout).")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Corrupted JSON request failed unexpectedly: {e}")

    # 4. Test client cancellation (timeout before 200ms sleep finishes)
    try:
        requests.post(f"{BASE_URL}/process", json={"data": "test"}, timeout=0.05)
    except requests.exceptions.Timeout:
        # This is expected, we are simulating a client cancellation
        pass
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Cancellation request failed unexpectedly: {e}")

    # Wait for the goroutine to potentially finish its 200ms sleep and attempt to send to channel
    time.sleep(0.5)

    # 5. Check final goroutine count
    final_goroutines = get_goroutines()

    # Allow at most N+1 transiently as per problem description
    assert final_goroutines <= baseline_goroutines + 1, \
        f"Goroutine leak detected! Baseline: {baseline_goroutines}, Final: {final_goroutines}"