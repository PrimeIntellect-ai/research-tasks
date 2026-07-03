# test_final_state.py

import pytest
import requests
import time

SERVICE_URL = "http://127.0.0.0:8080/api/v1/anomalies"
AUTH_HEADER = {"Authorization": "Bearer l10n-metrics-secret"}

def wait_for_service():
    """Wait for the service to become available."""
    for _ in range(10):
        try:
            requests.get("http://127.0.0.1:8080", timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    return False

def test_service_running():
    """Verify the service is running on port 8080."""
    # We check if the port is open by attempting a request
    try:
        response = requests.get(SERVICE_URL, headers=AUTH_HEADER, timeout=5)
        assert response.status_code in [200, 401, 403, 404, 500], "Service responded with an unexpected status code."
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 0.0.0.0:8080 or is unreachable.")

def test_unauthorized_access():
    """Verify the endpoint enforces Bearer token authentication."""
    response = requests.get(SERVICE_URL, timeout=5)
    assert response.status_code in [401, 403], f"Expected 401 or 403 for unauthorized access, got {response.status_code}"

def test_anomalies_endpoint_response():
    """Verify the endpoint returns the correct JSON structure and data."""
    response = requests.get(SERVICE_URL, headers=AUTH_HEADER, timeout=5)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON.")

    assert "anomalies" in data, "Response JSON missing 'anomalies' key."
    anomalies = data["anomalies"]

    assert isinstance(anomalies, list), "'anomalies' should be a list."

    expected_anomalies = [
        {
            "timestamp": 1714999860,
            "server_name": "server_B_metric",
            "metric_value": 91.5
        },
        {
            "timestamp": 1715000000,
            "server_name": "server_regional_1",
            "metric_value": 94.5
        },
        {
            "timestamp": 1715000060,
            "server_name": "server_regional_1",
            "metric_value": 98.2
        }
    ]

    # Check if the returned anomalies match the expected ones exactly
    assert len(anomalies) == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalies, got {len(anomalies)}."

    for i, expected in enumerate(expected_anomalies):
        actual = anomalies[i]
        assert actual.get("timestamp") == expected["timestamp"], f"Mismatch in timestamp at index {i}. Expected {expected['timestamp']}, got {actual.get('timestamp')}"
        assert actual.get("server_name") == expected["server_name"], f"Mismatch in server_name at index {i}. Expected {expected['server_name']}, got {actual.get('server_name')}"
        # Use a small tolerance for float comparison
        assert abs(float(actual.get("metric_value", 0)) - expected["metric_value"]) < 1e-5, f"Mismatch in metric_value at index {i}. Expected {expected['metric_value']}, got {actual.get('metric_value')}"