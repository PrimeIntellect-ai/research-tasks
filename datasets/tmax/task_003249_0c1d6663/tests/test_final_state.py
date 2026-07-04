# test_final_state.py
import os
import requests
import pytest

PORT = 8443
API_KEY = "super-secret-token-99"
BASE_URL = f"http://127.0.0.1:{PORT}"

def test_files_recovered_and_created():
    assert os.path.isfile("/home/user/server.py"), "/home/user/server.py was not recovered or is missing"
    assert os.path.isfile("/home/user/test_regression.py"), "/home/user/test_regression.py was not created"

def test_service_authentication():
    try:
        response_no_auth = requests.get(f"{BASE_URL}/logs", timeout=3)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {BASE_URL}. Is it running? Error: {e}")

    assert response_no_auth.status_code == 401, f"Expected HTTP 401 Unauthorized when no API key is provided, got {response_no_auth.status_code}"

    headers = {"X-API-KEY": API_KEY}
    response_auth = requests.get(f"{BASE_URL}/logs", headers=headers, timeout=3)
    assert response_auth.status_code == 200, f"Expected HTTP 200 OK with valid API key, got {response_auth.status_code}"

def test_service_boundary_condition_fixed():
    headers = {"X-API-KEY": API_KEY}
    payload = [{"msg": "log1"}, {"msg": "log2"}, {"msg": "log3"}]

    try:
        post_response = requests.post(f"{BASE_URL}/logs", headers=headers, json=payload, timeout=3)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to POST to the service at {BASE_URL}. Error: {e}")

    assert post_response.status_code == 200, f"Expected HTTP 200 OK on POST, got {post_response.status_code}"

    try:
        get_response = requests.get(f"{BASE_URL}/logs", headers=headers, timeout=3)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to GET from the service at {BASE_URL}. Error: {e}")

    assert get_response.status_code == 200, f"Expected HTTP 200 OK on GET, got {get_response.status_code}"

    data = get_response.json()
    assert "logs" in data, "Response JSON is missing the 'logs' key"

    logs = data["logs"]

    # Check if the last log entry was successfully processed and stored
    found_log3 = any(log.get("msg") == "log3" for log in logs)
    assert found_log3, "The last log entry ('log3') was not found in the stored logs. The off-by-one boundary condition bug is not fixed."