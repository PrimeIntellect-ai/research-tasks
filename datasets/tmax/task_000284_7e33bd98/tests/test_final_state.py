# test_final_state.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
ENDPOINT = f"{BASE_URL}/audit"
AUTH_TOKEN = "Bearer sec-audit-2024"

def test_missing_auth_header():
    """Test that the server returns 401 when the Authorization header is missing."""
    try:
        response = requests.get(ENDPOINT, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the server at {BASE_URL}. Is it running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}. Response: {response.text}"

def test_incorrect_auth_header():
    """Test that the server returns 401 when the Authorization header is incorrect."""
    headers = {"Authorization": "Bearer wrong-token"}
    try:
        response = requests.get(ENDPOINT, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the server at {BASE_URL}. Is it running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized for incorrect token, got {response.status_code}. Response: {response.text}"

def test_valid_request_processing():
    """Test that the server returns 200 and the correctly processed JSON data."""
    headers = {"Authorization": AUTH_TOKEN}
    try:
        response = requests.get(ENDPOINT, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the server at {BASE_URL}. Is it running?")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    expected_data = [
        {
            "timestamp": "2024-01-01T10:00:00Z",
            "user": "admin",
            "event_data": "User viewed &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;"
        },
        {
            "timestamp": "2024-01-01T10:05:00Z",
            "user": "hr_manager",
            "event_data": "Updated record for SSN [REDACTED_SSN] and [REDACTED_SSN]."
        }
    ]

    assert isinstance(data, list), f"Expected JSON response to be a list, got {type(data)}"
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in JSON array, got {len(data)}"

    for i, expected_item in enumerate(expected_data):
        actual_item = data[i]
        assert actual_item.get("timestamp") == expected_item["timestamp"], f"Mismatch in timestamp at index {i}. Expected {expected_item['timestamp']}, got {actual_item.get('timestamp')}"
        assert actual_item.get("user") == expected_item["user"], f"Mismatch in user at index {i}. Expected {expected_item['user']}, got {actual_item.get('user')}"
        assert actual_item.get("event_data") == expected_item["event_data"], f"Mismatch in event_data at index {i}. Expected {expected_item['event_data']}, got {actual_item.get('event_data')}"