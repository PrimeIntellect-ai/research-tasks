# test_final_state.py

import requests
import pytest
import time

BASE_URL = "http://127.0.0.1:8888"
COMPUTE_URL = f"{BASE_URL}/compute"
AUTH_TOKEN = "token_xyz_98765"
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}

def wait_for_service():
    """Wait for the service to be up and running."""
    max_retries = 10
    for _ in range(max_retries):
        try:
            # Just check if the port is open and responding to HTTP
            requests.get(BASE_URL, timeout=1)
            return
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    pytest.fail("Service is not running or not reachable at 127.0.0.1:8888")

@pytest.fixture(scope="module", autouse=True)
def setup():
    wait_for_service()

def test_authentication_required():
    """Test that the service requires the correct authentication token."""
    response = requests.post(COMPUTE_URL, json={"value": 10}, timeout=2)
    assert response.status_code in [401, 403], (
        f"Expected 401 or 403 for unauthenticated request, got {response.status_code}"
    )

def test_poison_pill_handling():
    """Test that the service handles the poison pill gracefully."""
    response = requests.post(COMPUTE_URL, json={"value": -1}, headers=HEADERS, timeout=2)
    assert response.status_code == 400, (
        f"Expected 400 Bad Request for poison pill payload, got {response.status_code}"
    )

def test_mathematical_correctness():
    """Test that the service computes the correct result using the extracted modulus."""
    response = requests.post(COMPUTE_URL, json={"value": 10}, headers=HEADERS, timeout=2)
    assert response.status_code == 200, (
        f"Expected 200 OK for valid payload, got {response.status_code}. Response: {response.text}"
    )

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "result" in data, "Response JSON is missing 'result' key"
    assert data["result"] == 99730, (
        f"Expected result to be 99730 (10 * 9973), got {data['result']}"
    )