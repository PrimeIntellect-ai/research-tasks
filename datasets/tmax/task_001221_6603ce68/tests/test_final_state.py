# test_final_state.py

import requests
import pytest
import time

BASE_URL = "http://127.0.0.1:5000"

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
def check_service_up():
    assert wait_for_service(f"{BASE_URL}/api/v1/builds/nonexistent"), "Flask service is not running on 127.0.0.1:5000"

def test_valid_flow():
    payload = {
        "flow": "STEP app\nREQUIRES lib\nSTEP lib\nREQUIRES base\nSTEP base"
    }
    response = requests.post(f"{BASE_URL}/api/v1/builds", json=payload)
    assert response.status_code == 200, f"Expected 200 OK for valid flow, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "build_id" in data, "Response JSON missing 'build_id'"
    build_id = data["build_id"]

    # Fetch the build plan
    get_response = requests.get(f"{BASE_URL}/api/v1/builds/{build_id}")
    assert get_response.status_code == 200, f"Expected 200 OK when fetching build plan, got {get_response.status_code}"

    get_data = get_response.json()
    assert "steps" in get_data, "Response JSON missing 'steps'"

    # Check topological sort
    expected_steps = ["base", "lib", "app"]
    assert get_data["steps"] == expected_steps, f"Expected steps {expected_steps}, got {get_data['steps']}"

def test_circular_dependency():
    payload = {
        "flow": "STEP ios\nREQUIRES macos\nSTEP macos\nREQUIRES ios"
    }
    response = requests.post(f"{BASE_URL}/api/v1/builds", json=payload)
    assert response.status_code == 400, f"Expected 400 Bad Request for circular dependency, got {response.status_code}"

    data = response.json()
    assert "error" in data, "Response JSON missing 'error' key"
    assert "circular dependency detected" in data["error"].lower(), f"Expected circular dependency error message, got: {data['error']}"

def test_get_nonexistent_build():
    response = requests.get(f"{BASE_URL}/api/v1/builds/invalid-uuid-1234")
    assert response.status_code == 404, f"Expected 404 Not Found for invalid build_id, got {response.status_code}"