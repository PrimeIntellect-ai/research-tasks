# test_final_state.py
import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"
AUTH_HEADER = {"Authorization": "Bearer ML-DATA-2024"}

def test_unauthenticated_request():
    try:
        response = requests.get(f"{BASE_URL}/generate?n=100", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for unauthenticated request, got {response.status_code}"

def test_authenticated_request_and_logic():
    try:
        response = requests.get(f"{BASE_URL}/generate?n=2000", headers=AUTH_HEADER, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for authenticated request, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "ks_distance" in data, "JSON response missing 'ks_distance' key"
    assert "samples" in data, "JSON response missing 'samples' key"

    ks_distance = data["ks_distance"]
    samples = data["samples"]

    assert isinstance(ks_distance, (int, float)), "ks_distance must be a number"
    assert isinstance(samples, list), "samples must be a list"
    assert len(samples) == 2000, f"Expected 2000 samples, got {len(samples)}"

    assert ks_distance < 0.05, f"KS distance {ks_distance} is too large. Expected < 0.05. Check sampling logic and baseline comparison."