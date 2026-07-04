# test_final_state.py

import pytest
import requests
import time

URL = "http://127.0.0.1:8080/api/v1/extract"

def wait_for_service():
    """Wait for the service to be up and running."""
    for _ in range(10):
        try:
            # We just check if the port is open and responding to HTTP
            requests.get("http://127.0.0.1:8080/", timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

@pytest.fixture(scope="session", autouse=True)
def ensure_service_running():
    assert wait_for_service(), "The Go service is not listening on 127.0.0.1:8080 or is not reachable."

def test_extract_old_version_1_0_0():
    headers = {"X-App-Version": "1.0.0"}
    response = requests.post(URL, headers=headers, timeout=2)
    assert response.status_code == 426, f"Expected HTTP 426 Upgrade Required for version 1.0.0, got {response.status_code}. Response: {response.text}"

def test_extract_old_version_2_0_9():
    headers = {"X-App-Version": "2.0.9"}
    response = requests.post(URL, headers=headers, timeout=2)
    assert response.status_code == 426, f"Expected HTTP 426 Upgrade Required for version 2.0.9, got {response.status_code}. Response: {response.text}"

def test_extract_valid_version_2_1_0():
    headers = {"X-App-Version": "2.1.0"}
    response = requests.post(URL, headers=headers, timeout=2)
    assert response.status_code == 200, f"Expected HTTP 200 OK for version 2.1.0, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("transmission_id") == 104, f"Expected transmission_id=104, got {data.get('transmission_id')}"
    assert data.get("transcript") == "Eagle has landed", f"Expected transcript='Eagle has landed', got {data.get('transcript')}"
    assert data.get("migrated") is True, f"Expected migrated=True, got {data.get('migrated')}"

def test_extract_valid_version_2_1_0_beta():
    headers = {"X-App-Version": "2.1.0-beta"}
    response = requests.post(URL, headers=headers, timeout=2)
    assert response.status_code == 200, f"Expected HTTP 200 OK for version 2.1.0-beta, got {response.status_code}. Response: {response.text}"