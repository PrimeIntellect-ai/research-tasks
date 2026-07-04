# test_final_state.py
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer ds-secret-token-42"}

def test_metrics_no_auth():
    """Verify that /metrics endpoint requires authorization."""
    try:
        response = requests.get(f"{BASE_URL}/metrics", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /metrics: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without auth token, got {response.status_code}"

def test_metrics_with_auth():
    """Verify that /metrics returns the correct JSON structure and valid values."""
    try:
        response = requests.get(f"{BASE_URL}/metrics", headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /metrics: {e}")

    assert response.status_code == 200, f"Expected 200 OK with auth token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /metrics is not valid JSON. Response: {response.text}")

    assert "singular_value_1" in data, "Missing 'singular_value_1' in JSON response"
    assert "kl_divergence" in data, "Missing 'kl_divergence' in JSON response"

    assert isinstance(data["singular_value_1"], (int, float)), "singular_value_1 must be a number"
    assert isinstance(data["kl_divergence"], (int, float)), "kl_divergence must be a number"

    assert data["singular_value_1"] > 0, f"singular_value_1 should be > 0, got {data['singular_value_1']}"
    assert data["kl_divergence"] > 0, f"kl_divergence should be > 0, got {data['kl_divergence']}"

def test_compare_no_auth():
    """Verify that /compare endpoint requires authorization."""
    payload = {"reference": [1, 2, 3], "test": [2, 3, 4]}
    try:
        response = requests.post(f"{BASE_URL}/compare", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /compare: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without auth token, got {response.status_code}"

def test_compare_with_auth():
    """Verify that /compare computes the correct Wasserstein distance."""
    payload = {
        "reference": [1, 2, 3],
        "test": [2, 3, 4]
    }
    try:
        response = requests.post(f"{BASE_URL}/compare", headers=AUTH_HEADER, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /compare: {e}")

    assert response.status_code == 200, f"Expected 200 OK with auth token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /compare is not valid JSON. Response: {response.text}")

    assert "wasserstein_distance" in data, "Missing 'wasserstein_distance' in JSON response"

    wd = data["wasserstein_distance"]
    assert isinstance(wd, (int, float)), "wasserstein_distance must be a number"
    assert abs(wd - 1.0) < 1e-5, f"Expected wasserstein_distance to be approx 1.0, got {wd}"