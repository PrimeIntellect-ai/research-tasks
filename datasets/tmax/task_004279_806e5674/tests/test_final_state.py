# test_final_state.py
import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def wait_for_service(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(url)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    return False

@pytest.fixture(scope="module", autouse=True)
def check_service_running():
    assert wait_for_service(f"{BASE_URL}/status"), "The service is not running or not reachable on 127.0.0.1:8000."

def test_status_missing_headers():
    response = requests.get(f"{BASE_URL}/status")
    assert response.status_code == 400, f"Expected HTTP 400 for missing headers, got {response.status_code}"

def test_status_valid_credentials():
    headers = {
        "X-Override-Code": "OMEGA77",
        "X-Session-Id": "9928374"
    }
    response = requests.get(f"{BASE_URL}/status", headers=headers)
    assert response.status_code == 200, f"Expected HTTP 200 for valid credentials, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert data.get("status") == "recovered", f"Expected JSON payload {{'status': 'recovered'}}, got {data}"

def test_status_invalid_credentials():
    headers = {
        "X-Override-Code": "INVALID",
        "X-Session-Id": "0000000"
    }
    response = requests.get(f"{BASE_URL}/status", headers=headers)
    # The instructions don't explicitly specify the status for incorrect headers, 
    # but it shouldn't be 200 and shouldn't crash (500). Usually 403 or 401 or 400.
    assert response.status_code != 200, "Expected non-200 status code for invalid credentials"
    assert response.status_code != 500, "Service crashed (HTTP 500) with invalid credentials"