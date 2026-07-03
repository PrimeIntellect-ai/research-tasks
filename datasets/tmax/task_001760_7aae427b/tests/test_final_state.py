# test_final_state.py
import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8080/api/v1/records/USR-9942A"
TOKEN = "SEC-7719-XY"

@pytest.fixture(scope="module", autouse=True)
def wait_for_server():
    """Wait for the API server to be up and running."""
    max_retries = 10
    for _ in range(max_retries):
        try:
            # Just test connection
            requests.get("http://127.0.0.1:8080/", timeout=1)
            return
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    # If we can't connect to the root, we'll let the actual tests fail, but it's better to try the specific endpoint.

def test_api_server_running_and_fixed_bug():
    """Test that the API server handles the previously buggy payload without a 500 error."""
    params = {"token": TOKEN}
    payload = {"include_archived": True, "sort": "desc"}

    try:
        response = requests.get(BASE_URL, params=params, json=payload, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("API server is not running or not listening on 127.0.0.1:8080")

    assert response.status_code != 500, f"Server returned 500 Internal Server Error for payload {payload}"
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def test_api_server_full_payload():
    """Test that the API server handles the full payload without a 500 error."""
    params = {"token": TOKEN}
    payload = {
        "include_archived": True, 
        "sort": "desc", 
        "limit": 100, 
        "status": "pending"
    }

    try:
        response = requests.get(BASE_URL, params=params, json=payload, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("API server is not running or not listening on 127.0.0.1:8080")

    assert response.status_code != 500, f"Server returned 500 Internal Server Error for full payload {payload}"
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def test_api_server_other_combinations():
    """Test other combinations to ensure no regressions."""
    params = {"token": TOKEN}
    payloads = [
        {"include_archived": False, "sort": "desc"},
        {"include_archived": True, "sort": "asc"},
        {"limit": 10, "status": "approved"}
    ]

    for payload in payloads:
        try:
            response = requests.get(BASE_URL, params=params, json=payload, timeout=2)
        except requests.exceptions.ConnectionError:
            pytest.fail("API server is not running or not listening on 127.0.0.1:8080")

        assert response.status_code != 500, f"Server returned 500 Internal Server Error for payload {payload}"
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"