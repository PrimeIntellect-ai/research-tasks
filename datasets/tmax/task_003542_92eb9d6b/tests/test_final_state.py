# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_api_frequency():
    url = f"{BASE_URL}/api/frequency"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    assert "frequency" in data, "Response missing 'frequency' key"
    assert "ci_lower" in data, "Response missing 'ci_lower' key"
    assert "ci_upper" in data, "Response missing 'ci_upper' key"

    freq = data["frequency"]
    ci_lower = data["ci_lower"]
    ci_upper = data["ci_upper"]

    assert isinstance(freq, (int, float)), "Frequency must be a number"
    assert isinstance(ci_lower, (int, float)), "ci_lower must be a number"
    assert isinstance(ci_upper, (int, float)), "ci_upper must be a number"

    # The true frequency is 3.5 Hz
    assert 3.0 <= freq <= 4.0, f"Expected frequency around 3.5 Hz, got {freq}"
    assert ci_lower <= ci_upper, "ci_lower must be <= ci_upper"

def test_api_velocity():
    frame_idx = 10
    url = f"{BASE_URL}/api/velocity?frame={frame_idx}"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    assert "velocity" in data, "Response missing 'velocity' key"

    vel = data["velocity"]
    assert isinstance(vel, (int, float)), "Velocity must be a number"

def test_api_reference_diff_unauthorized():
    url = f"{BASE_URL}/api/reference_diff"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for missing token, got {response.status_code}"

def test_api_reference_diff_authorized():
    url = f"{BASE_URL}/api/reference_diff"
    headers = {"Authorization": "Bearer data-sci-token-882"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    assert "mse" in data, "Response missing 'mse' key"

    mse = data["mse"]
    assert isinstance(mse, (int, float)), "MSE must be a number"
    assert mse >= 0, "MSE cannot be negative"