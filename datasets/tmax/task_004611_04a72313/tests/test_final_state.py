# test_final_state.py
import requests
import pytest

API_URL = "http://127.0.0.1:8080/deadlock-analysis"
AUTH_TOKEN = "Omega-92-Delta"
EXPECTED_TARGET_USER = "U-7734"
EXPECTED_DEADLOCKED_USER = "U-1022"
EXPECTED_RESOURCES = ["RES-A", "RES-B"]

def test_api_unauthorized():
    """Test that the API rejects requests without the correct Bearer token."""
    try:
        response = requests.get(API_URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {API_URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_api_invalid_token():
    """Test that the API rejects requests with an invalid Bearer token."""
    headers = {"Authorization": "Bearer Invalid-Token-123"}
    try:
        response = requests.get(API_URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {API_URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized with invalid token, got {response.status_code}"

def test_api_authorized_and_response():
    """Test that the API accepts the correct Bearer token and returns the expected JSON."""
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    try:
        response = requests.get(API_URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {API_URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "target_user" in data, "Missing 'target_user' in response JSON"
    assert data["target_user"] == EXPECTED_TARGET_USER, f"Expected target_user '{EXPECTED_TARGET_USER}', got '{data['target_user']}'"

    assert "deadlocked_with_user" in data, "Missing 'deadlocked_with_user' in response JSON"
    assert data["deadlocked_with_user"] == EXPECTED_DEADLOCKED_USER, f"Expected deadlocked_with_user '{EXPECTED_DEADLOCKED_USER}', got '{data['deadlocked_with_user']}'"

    assert "resources_involved" in data, "Missing 'resources_involved' in response JSON"
    assert isinstance(data["resources_involved"], list), "'resources_involved' must be a list"

    # The specification requires alphabetical sorting
    assert data["resources_involved"] == EXPECTED_RESOURCES, f"Expected resources_involved {EXPECTED_RESOURCES} (sorted), got {data['resources_involved']}"