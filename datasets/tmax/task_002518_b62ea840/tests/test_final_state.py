# test_final_state.py

import pytest
import requests

def test_api_investigate_endpoint():
    url = "http://127.0.0.1:8080/api/investigate"
    payload = {"video_ping_ids": [45, 120, 315]}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API service at {url}. Is the service running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, but got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "suspect_drivers" in data, f"Key 'suspect_drivers' missing from response. Response data: {data}"

    expected_drivers = ["Alice", "Charlie"]
    actual_drivers = data["suspect_drivers"]

    assert isinstance(actual_drivers, list), f"Expected 'suspect_drivers' to be a list, got {type(actual_drivers)}"
    assert actual_drivers == expected_drivers, f"Expected suspect drivers {expected_drivers}, but got {actual_drivers}"