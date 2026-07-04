# test_final_state.py

import pytest
import requests
import concurrent.futures
import time

BASE_URL = "http://127.0.0.1:8080"
HEADERS = {"Authorization": "Bearer calc-token-998"}

def wait_for_service():
    """Wait for the service to be available."""
    for _ in range(10):
        try:
            # Send a request without auth to check if it's up
            resp = requests.post(f"{BASE_URL}/sum", json={"data": []}, timeout=1)
            if resp.status_code in [401, 403, 422, 200]:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    return False

@pytest.fixture(scope="module", autouse=True)
def ensure_service_running():
    assert wait_for_service(), f"Service is not reachable at {BASE_URL}"

def test_unauthorized_access():
    """Test that missing or incorrect token returns 401."""
    resp_missing = requests.post(f"{BASE_URL}/sum", json={"data": [1.0, 2.0]})
    assert resp_missing.status_code in [401, 403], f"Expected 401/403 for missing token, got {resp_missing.status_code}"

    resp_invalid = requests.post(
        f"{BASE_URL}/sum", 
        json={"data": [1.0, 2.0]}, 
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert resp_invalid.status_code in [401, 403], f"Expected 401/403 for invalid token, got {resp_invalid.status_code}"

def test_sum_precision():
    """Test that the /sum endpoint correctly handles precision issues."""
    data = {"data": [1e16, 1.0, -1e16]}
    resp = requests.post(f"{BASE_URL}/sum", json=data, headers=HEADERS)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}: {resp.text}"

    result = resp.json().get("result")
    assert result is not None, "Response JSON missing 'result' key"
    assert result == 1.0, f"Expected sum result 1.0, got {result}. Precision bug not fixed."

def test_variance_concurrency():
    """Test that the /variance endpoint handles concurrent requests correctly."""
    # Population variance of [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0] is 4.0
    payload = {"data": [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]}

    def make_request():
        resp = requests.post(f"{BASE_URL}/variance", json=payload, headers=HEADERS)
        if resp.status_code != 200:
            return None, resp.status_code
        return resp.json().get("result"), resp.status_code

    num_requests = 50
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    for val, status in results:
        assert status == 200, f"Expected 200 OK during concurrent requests, got {status}"
        assert val is not None, "Response JSON missing 'result' key during concurrent requests"
        assert abs(val - 4.0) < 1e-7, f"Expected variance 4.0, got {val}. Concurrency bug not fixed."