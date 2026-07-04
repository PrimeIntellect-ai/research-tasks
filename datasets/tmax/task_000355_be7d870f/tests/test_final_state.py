# test_final_state.py

import math
import requests
import pytest

def test_api_data_response():
    url = "http://127.0.0.1:8080/api/data"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the web service at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, but failed to parse. Response text: {response.text}")

    assert "id" in data, "Response JSON is missing the 'id' key."
    assert "calibrated_value" in data, "Response JSON is missing the 'calibrated_value' key."

    assert data["id"] == 105, f"Expected id to be 105, got {data['id']}"

    expected_value = 42.1234
    actual_value = data["calibrated_value"]

    assert isinstance(actual_value, (int, float)), f"Expected 'calibrated_value' to be a number, got {type(actual_value)}"
    assert math.isclose(actual_value, expected_value, rel_tol=1e-5), f"Expected calibrated_value to be close to {expected_value}, got {actual_value}"