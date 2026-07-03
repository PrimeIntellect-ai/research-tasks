# test_final_state.py
import pytest
import requests
import time
import math

BASE_URL = "http://127.0.0.1:8080"
HEADERS = {"Authorization": "Bearer secret_ts_2024"}

def wait_for_server():
    """Wait for the server to be available."""
    for _ in range(10):
        try:
            requests.get(BASE_URL)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    return False

@pytest.fixture(scope="module", autouse=True)
def ensure_server_running():
    assert wait_for_server(), "Server is not listening on port 8080."

def test_unauthorized_access():
    """Test that missing or invalid auth headers return 401."""
    endpoints = ["/api/telemetry", "/api/mae"]
    for ep in endpoints:
        resp_no_auth = requests.get(BASE_URL + ep)
        assert resp_no_auth.status_code == 401, f"Expected 401 for {ep} without auth, got {resp_no_auth.status_code}"

        resp_bad_auth = requests.get(BASE_URL + ep, headers={"Authorization": "Bearer wrong_token"})
        assert resp_bad_auth.status_code == 401, f"Expected 401 for {ep} with bad auth, got {resp_bad_auth.status_code}"

def test_telemetry_endpoint():
    """Test the /api/telemetry endpoint returns the correct masked operator and interpolated data."""
    resp = requests.get(BASE_URL + "/api/telemetry", headers=HEADERS)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

    data = resp.json()
    assert "operator" in data, "Response missing 'operator' field"
    assert data["operator"] == "MASKED", f"Expected operator to be 'MASKED', got {data['operator']}"

    assert "data" in data, "Response missing 'data' field"

    expected_data = [
        {"time": 0, "value": 20.0},
        {"time": 10, "value": 22.0},
        {"time": 20, "value": 24.0},
        {"time": 30, "value": 26.0},
        {"time": 40, "value": 28.0},
        {"time": 50, "value": 30.0}
    ]

    actual_data = data["data"]
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} data points, got {len(actual_data)}"

    for expected, actual in zip(expected_data, actual_data):
        assert actual["time"] == expected["time"], f"Expected time {expected['time']}, got {actual['time']}"
        assert math.isclose(actual["value"], expected["value"], rel_tol=1e-3), \
            f"Expected value {expected['value']} at time {expected['time']}, got {actual['value']}"

def test_mae_endpoint():
    """Test the /api/mae endpoint returns the correct Mean Absolute Error."""
    resp = requests.get(BASE_URL + "/api/mae", headers=HEADERS)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

    data = resp.json()
    assert "mae" in data, "Response missing 'mae' field"

    expected_mae = 4.0 / 6.0
    actual_mae = data["mae"]

    assert math.isclose(actual_mae, expected_mae, rel_tol=1e-3), \
        f"Expected MAE ~{expected_mae}, got {actual_mae}"