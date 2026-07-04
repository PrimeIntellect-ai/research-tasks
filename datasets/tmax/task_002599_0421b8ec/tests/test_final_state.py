# test_final_state.py
import pytest
import requests

def test_unauthorized_wrong_token():
    url = "http://127.0.0.1:8080/api/analyze"
    headers = {"Authorization": "Bearer WRONG_TOKEN"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or request timed out: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for wrong token, got {response.status_code}"

def test_unauthorized_missing_token():
    url = "http://127.0.0.1:8080/api/analyze"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or request timed out: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing token, got {response.status_code}"

def test_authorized_and_response_validation():
    url = "http://127.0.0.1:8080/api/analyze"
    headers = {"Authorization": "Bearer XY88-SPEC-9Z"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or request timed out: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for correct token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    for key in ["peak_x", "ci_95_low", "ci_95_high"]:
        assert key in data, f"Missing key '{key}' in JSON response: {data}"
        assert isinstance(data[key], (int, float)), f"Key '{key}' must be a number, got {type(data[key])}"

    peak_x = float(data["peak_x"])
    ci_95_low = float(data["ci_95_low"])
    ci_95_high = float(data["ci_95_high"])

    assert 48.0 <= peak_x <= 52.0, f"peak_x {peak_x} is out of expected bounds [48.0, 52.0]"
    assert ci_95_low <= peak_x, f"ci_95_low {ci_95_low} should be <= peak_x {peak_x}"
    assert ci_95_high >= peak_x, f"ci_95_high {ci_95_high} should be >= peak_x {peak_x}"