# test_final_state.py

import requests
import pytest

URL = "http://127.0.0.1:8080/api/targets"
TOKEN = "LAB-TKN-8891A"

def test_server_unauthorized():
    """Test that the server returns 401 Unauthorized when no token is provided."""
    try:
        response = requests.get(URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, but got {response.status_code}. Response: {response.text}"

def test_server_authorized_and_data():
    """Test that the server returns 200 OK with the correct JSON data when authorized."""
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    try:
        response = requests.get(URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid auth, but got {response.status_code}. Response: {response.text}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type to contain application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Failed to parse response body as JSON. Response text: {response.text}")

    assert isinstance(data, list), f"Expected response JSON to be a list, got {type(data).__name__}"
    assert len(data) == 2, f"Expected exactly 2 objects in the JSON array, got {len(data)}"

    expected_objects = [
        {"id": 101, "is_research_target": True, "name": "sample_A"},
        {"id": 103, "is_research_target": True, "name": "sample_C"}
    ]

    # Check if all expected objects are in the response (order does not matter)
    for expected in expected_objects:
        assert expected in data, f"Expected object {expected} not found in response data: {data}"