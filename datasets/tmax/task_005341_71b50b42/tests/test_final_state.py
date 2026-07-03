# test_final_state.py

import pytest
import requests

URL = "http://127.0.0.1:9090/api/v1/latest-backups"
TOKEN = "DBRE_SECURE_8832"

def test_api_unauthorized():
    """Verify that the API rejects requests without a valid token."""
    # Test without header
    try:
        response = requests.get(URL, timeout=5)
        assert response.status_code in (401, 403), f"Expected 401/403 without token, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    # Test with wrong token
    try:
        headers = {"Authorization": "Bearer WRONG_TOKEN"}
        response = requests.get(URL, headers=headers, timeout=5)
        assert response.status_code in (401, 403), f"Expected 401/403 with wrong token, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

def test_api_success_and_data():
    """Verify that the API returns the correct aggregated backup data with a valid token."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(URL, headers=headers, timeout=5)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

        assert isinstance(data, list), "Expected JSON response to be a list"

        expected_data = [
            {
                "device_name": "Server-A",
                "latest_status": "SUCCESS",
                "timestamp": "2023-10-02 10:00:00"
            },
            {
                "device_name": "Server-B",
                "latest_status": "SUCCESS",
                "timestamp": "2023-10-01 11:00:00"
            }
        ]

        # Sort both lists by device_name to compare regardless of order
        data_sorted = sorted(data, key=lambda x: x.get("device_name", ""))
        expected_sorted = sorted(expected_data, key=lambda x: x["device_name"])

        assert data_sorted == expected_sorted, f"Expected {expected_sorted}, but got {data_sorted}"

    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")