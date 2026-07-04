# test_final_state.py

import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="session", autouse=True)
def wait_for_server():
    """Wait for the HTTP server to become available."""
    timeout = 10
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{BASE_URL}/api/report", timeout=1)
            # We don't assert status here, just that the connection is accepted
            return
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    pytest.fail(f"Server did not start on {BASE_URL} within {timeout} seconds.")

def test_api_report_endpoint():
    url = f"{BASE_URL}/api/report"
    response = requests.get(url, timeout=5)

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type to be application/json"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    assert isinstance(data, list), f"Expected a JSON array, got {type(data).__name__}"

    expected_records = [
        {"backup_id": "B-100", "dc_name": "US-EAST-1", "status": "SUCCESS"},
        {"backup_id": "B-101", "dc_name": "EU-WEST-1", "status": "FAILED"},
        {"backup_id": "B-103", "dc_name": "AP-SOUTH-1", "status": "SUCCESS"}
    ]

    assert len(data) == len(expected_records), f"Expected {len(expected_records)} records, got {len(data)}. Data: {data}"

    # Sort both to compare regardless of order
    sorted_actual = sorted(data, key=lambda x: x.get("backup_id", ""))
    sorted_expected = sorted(expected_records, key=lambda x: x["backup_id"])

    assert sorted_actual == sorted_expected, f"Report data mismatch. Expected: {sorted_expected}, Actual: {sorted_actual}"

def test_api_route_endpoint():
    url = f"{BASE_URL}/api/route?src=US-EAST-1&dst=AP-SOUTH-1"
    response = requests.get(url, timeout=5)

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type to be application/json"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    assert isinstance(data, dict), f"Expected a JSON object, got {type(data).__name__}"

    expected_path = ["US-EAST-1", "EU-WEST-1", "AP-SOUTH-1"]
    expected_latency = 210

    assert data.get("path") == expected_path, f"Expected path {expected_path}, got {data.get('path')}"
    assert data.get("total_latency") == expected_latency, f"Expected total_latency {expected_latency}, got {data.get('total_latency')}"