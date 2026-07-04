# test_final_state.py

import requests
import pytest

BASE_URL = "http://127.0.0.1:8080/api/v1/user-activity"
AUTH_HEADER = {"Authorization": "Bearer etl-secret-token"}

def test_unauthorized_request():
    """Verify that a request without the auth header returns 401."""
    try:
        response = requests.get(BASE_URL, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Flask service is not running or not listening on 127.0.0.1:8080.")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}. Response: {response.text}"

def test_authorized_request():
    """Verify that a request with the valid auth header returns 200 and correct JSON."""
    try:
        response = requests.get(BASE_URL, headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Flask service is not running or not listening on 127.0.0.1:8080.")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON.")

    assert isinstance(data, list), "Expected response to be a JSON array (list)."

    # Verify specific user data
    bob = next((u for u in data if u.get("user_id") == 2), None)
    alice = next((u for u in data if u.get("user_id") == 1), None)

    assert bob is not None, "User 'bob' (user_id: 2) is missing from the response."
    assert alice is not None, "User 'alice' (user_id: 1) is missing from the response."

    assert bob.get("username") == "bob", "Incorrect username for user_id 2."
    assert bob.get("department") == "engineering", "Incorrect department for user_id 2."
    assert bob.get("total_duration") == 300, f"Expected total_duration 300 for bob, got {bob.get('total_duration')}."
    assert bob.get("department_rank") == 1, f"Expected department_rank 1 for bob, got {bob.get('department_rank')}."

    assert alice.get("username") == "alice", "Incorrect username for user_id 1."
    assert alice.get("department") == "engineering", "Incorrect department for user_id 1."
    assert alice.get("total_duration") == 120, f"Expected total_duration 120 for alice, got {alice.get('total_duration')}."
    assert alice.get("department_rank") == 2, f"Expected department_rank 2 for alice, got {alice.get('department_rank')}."