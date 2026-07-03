# test_final_state.py

import pytest
import requests
import math

BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = f"{BASE_URL}/process"
AUTH_HEADER = {"Authorization": "Bearer h3x-f0r3ns1cs"}

def test_auth_missing():
    payload = {"sensor_id": "TEST_AUTH", "data": [1.0, 2.0]}
    try:
        response = requests.post(ENDPOINT, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}"

def test_auth_incorrect():
    payload = {"sensor_id": "TEST_AUTH", "data": [1.0, 2.0]}
    headers = {"Authorization": "Bearer wrong-token"}
    try:
        response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for incorrect auth, got {response.status_code}"

def test_process_zero_variance_with_padding():
    payload = {"sensor_id": "TEST1", "data": [10.0, 10.0, "error", None, 10.0]}
    try:
        response = requests.post(ENDPOINT, json=payload, headers=AUTH_HEADER, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Body: {response.text}"

    data = response.json()
    assert "sensor_id" in data, "Response missing 'sensor_id'"
    assert "final_score" in data, "Response missing 'final_score'"
    assert data["sensor_id"] == "TEST1", f"Expected sensor_id 'TEST1', got {data['sensor_id']}"

    expected_score = 6000000.0
    assert math.isclose(data["final_score"], expected_score, rel_tol=1e-3), \
        f"Expected final_score ~ {expected_score}, got {data['final_score']}"

def test_process_normal_variance_with_truncation():
    payload = {"sensor_id": "TEST2", "data": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, "invalid"]}
    try:
        response = requests.post(ENDPOINT, json=payload, headers=AUTH_HEADER, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Body: {response.text}"

    data = response.json()
    assert data["sensor_id"] == "TEST2", f"Expected sensor_id 'TEST2', got {data.get('sensor_id')}"

    # Cleaned data: [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    # Mean: 3.5
    # Variance: ((2.5^2)*2 + (1.5^2)*2 + (0.5^2)*2)/6 = 17.5 / 6 = 2.9166666666666665
    # Variance + 1e-6 = 2.9166676666666665
    # inv_var = 1.0 / 2.9166676666666665 = 0.3428570204
    # Binary args: 1.0 2.0 3.0 4.0 5.0 -> 0.1 + 0.4 + 0.9 + 1.6 + 2.5 = 5.5
    # Final score: 5.5 * 0.3428570204 = 1.8857136
    expected_score = 1.8857136
    assert math.isclose(data["final_score"], expected_score, rel_tol=1e-3), \
        f"Expected final_score ~ {expected_score}, got {data.get('final_score')}"