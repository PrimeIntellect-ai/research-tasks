# test_final_state.py
import requests
import pytest
import math

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer RES-994"}

def test_unauthorized_access():
    """Test that requests without the correct authorization header are rejected."""
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/stats: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized without auth header, got {response.status_code}"

def test_stats_endpoint():
    """Test the /stats endpoint returns correct statistical results."""
    try:
        response = requests.get(f"{BASE_URL}/stats", headers=AUTH_HEADER, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/stats: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK from /stats, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /stats is not valid JSON. Response text: {response.text}")

    assert "slope" in data, "Missing 'slope' key in /stats response"
    assert "bootstrap_ci_lower" in data, "Missing 'bootstrap_ci_lower' key in /stats response"
    assert "bootstrap_ci_upper" in data, "Missing 'bootstrap_ci_upper' key in /stats response"

    try:
        slope = float(data["slope"])
    except (ValueError, TypeError):
        pytest.fail(f"Slope value '{data['slope']}' cannot be converted to float.")

    assert math.isclose(slope, 2.0114, abs_tol=0.01), f"Reported slope {slope} is not within 0.01 tolerance of 2.0114"

def test_data_endpoint():
    """Test the /data endpoint returns the correct cleaned dataset."""
    try:
        response = requests.get(f"{BASE_URL}/data", headers=AUTH_HEADER, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/data: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK from /data, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /data is not valid JSON. Response text: {response.text}")

    assert isinstance(data, list), f"Response from /data should be a JSON array, got {type(data).__name__}"

    expected_data = [
        {"alpha": 1.0, "beta": 2.1},
        {"alpha": 2.0, "beta": 3.9},
        {"alpha": 3.0, "beta": 6.2},
        {"alpha": 4.0, "beta": 8.0},
        {"alpha": 5.0, "beta": 9.9},
        {"alpha": 6.0, "beta": 12.1}
    ]

    assert len(data) == 6, f"Expected 6 valid data points, got {len(data)}. Ensure invalid observations are dropped."

    for expected in expected_data:
        found = False
        for item in data:
            if "alpha" in item and "beta" in item:
                try:
                    alpha_val = float(item["alpha"])
                    beta_val = float(item["beta"])
                    if math.isclose(alpha_val, expected["alpha"], abs_tol=0.001) and \
                       math.isclose(beta_val, expected["beta"], abs_tol=0.001):
                        found = True
                        break
                except (ValueError, TypeError):
                    continue
        assert found, f"Expected data point {expected} not found in /data response"