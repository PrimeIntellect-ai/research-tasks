# test_final_state.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:9090"
AUTH_HEADER = {"Authorization": "Bearer SOC-Analyst-2024"}

def test_api_unauthorized_no_header():
    """Test that requests without an authorization header are rejected with 401."""
    try:
        response = requests.get(f"{BASE_URL}/api/threats?dept=Engineering", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth header, got {response.status_code}"

def test_api_unauthorized_wrong_token():
    """Test that requests with an incorrect authorization header are rejected with 401."""
    try:
        response = requests.get(
            f"{BASE_URL}/api/threats?dept=Engineering", 
            headers={"Authorization": "Bearer Wrong-Token"},
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for wrong auth token, got {response.status_code}"

def test_api_threats_engineering():
    """Test that the API returns the correct deduplicated logs for Engineering."""
    try:
        response = requests.get(
            f"{BASE_URL}/api/threats?dept=Engineering", 
            headers=AUTH_HEADER,
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert isinstance(data, list), "Response should be a JSON array"

    expected_data = [
        {
            "timestamp": "2024-01-01T10:00:00Z",
            "ip_address": "192.168.1.10",
            "department": "Engineering",
            "error_code": 9021,
            "message": "Intrusion attempt ErrCode:9021"
        },
        {
            "timestamp": "2024-01-01T10:10:00Z",
            "ip_address": "192.168.1.10",
            "department": "Engineering",
            "error_code": 9999,
            "message": "Data exfiltration ErrCode:9999"
        }
    ]

    # Sort both lists by timestamp to ensure order doesn't cause false failures
    data_sorted = sorted(data, key=lambda x: x.get("timestamp", ""))
    expected_sorted = sorted(expected_data, key=lambda x: x["timestamp"])

    # Check length first to ensure deduplication worked
    assert len(data_sorted) == len(expected_sorted), f"Expected {len(expected_sorted)} records (deduplicated), got {len(data_sorted)}"

    # Compare each record
    for actual, expected in zip(data_sorted, expected_sorted):
        assert int(actual.get("error_code", -1)) == expected["error_code"], f"Error code mismatch: expected {expected['error_code']}, got {actual.get('error_code')}"
        for key in ["timestamp", "ip_address", "department", "message"]:
            assert actual.get(key) == expected[key], f"Mismatch in {key}: expected {expected[key]}, got {actual.get(key)}"

def test_api_threats_finance():
    """Test that the API returns the correct logs for Finance."""
    try:
        response = requests.get(
            f"{BASE_URL}/api/threats?dept=Finance", 
            headers=AUTH_HEADER,
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert isinstance(data, list), "Response should be a JSON array"
    assert len(data) == 1, f"Expected exactly 1 record for Finance, got {len(data)}"

    record = data[0]
    expected = {
        "timestamp": "2024-01-01T10:05:00Z",
        "ip_address": "10.0.0.5",
        "department": "Finance",
        "error_code": 404,
        "message": "Malformed packet ErrCode:404"
    }

    assert int(record.get("error_code", -1)) == expected["error_code"], "Error code mismatch"
    for key in ["timestamp", "ip_address", "department", "message"]:
        assert record.get(key) == expected[key], f"Mismatch in {key}"