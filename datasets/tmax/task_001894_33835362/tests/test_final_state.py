# test_final_state.py
import pytest
import requests
import time

URL = "http://127.0.0.1:8080/api/v1/drift"
HEADERS = {"Authorization": "Bearer devops-secret-token"}

def wait_for_server():
    """Wait for the Go server to start."""
    for _ in range(10):
        try:
            requests.get("http://127.0.0.1:8080/")
            return
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)

@pytest.fixture(autouse=True)
def setup_server():
    wait_for_server()

def test_auth_failure():
    payload = {"hostname": "core-db-primary", "cores": 64, "memory_gb": 256, "storage": "NVMe"}
    try:
        response = requests.post(URL, json=payload, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the Go server on 127.0.0.1:8080.")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}"

def test_validation_failure():
    payload = {"hostname": "core-db-primary", "cores": 0, "memory_gb": 256, "storage": "NVMe"}
    response = requests.post(URL, json=payload, headers=HEADERS, timeout=2)

    assert response.status_code == 400, f"Expected HTTP 400 for invalid payload, got {response.status_code}"
    data = response.json()
    assert data.get("status") == "invalid", f"Expected status 'invalid', got {data.get('status')}"

def test_zero_drift():
    payload = {"hostname": "core-db-primary", "cores": 64, "memory_gb": 256, "storage": "nvme"}
    response = requests.post(URL, json=payload, headers=HEADERS, timeout=2)

    assert response.status_code == 200, f"Expected HTTP 200 for zero drift, got {response.status_code}"
    data = response.json()
    assert data.get("status") == "valid", f"Expected status 'valid', got {data.get('status')}"
    assert data.get("total_drift") == 0, f"Expected total_drift 0, got {data.get('total_drift')}"

def test_calculated_drift():
    payload = {"hostname": "core-db-replica", "cores": 32, "memory_gb": 128, "storage": "SSD"}
    response = requests.post(URL, json=payload, headers=HEADERS, timeout=2)

    assert response.status_code == 200, f"Expected HTTP 200 for calculated drift, got {response.status_code}"
    data = response.json()
    assert data.get("status") == "valid", f"Expected status 'valid', got {data.get('status')}"
    assert data.get("total_drift") == 217, f"Expected total_drift 217, got {data.get('total_drift')}"