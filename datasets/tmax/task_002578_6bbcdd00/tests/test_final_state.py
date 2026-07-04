# test_final_state.py
import requests
import pytest

def test_api_result():
    url = "http://127.0.0.1:8080/api/result"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response: {response.text}")

    expected_keys = {"slope", "ci_lower", "ci_upper"}
    assert expected_keys.issubset(data.keys()), f"JSON response is missing required keys. Expected {expected_keys}, got {set(data.keys())}"

    slope = data["slope"]
    ci_lower = data["ci_lower"]
    ci_upper = data["ci_upper"]

    assert isinstance(slope, (int, float)), f"slope must be a number, got {type(slope)}"
    assert isinstance(ci_lower, (int, float)), f"ci_lower must be a number, got {type(ci_lower)}"
    assert isinstance(ci_upper, (int, float)), f"ci_upper must be a number, got {type(ci_upper)}"

    assert abs(slope - 3.140) <= 0.05, f"slope {slope} is not within tolerance of expected value ~3.140"
    assert abs(ci_lower - 3.100) <= 0.05, f"ci_lower {ci_lower} is not within tolerance of expected value ~3.100"
    assert abs(ci_upper - 3.180) <= 0.05, f"ci_upper {ci_upper} is not within tolerance of expected value ~3.180"
    assert ci_lower <= ci_upper, f"ci_lower {ci_lower} should be less than or equal to ci_upper {ci_upper}"