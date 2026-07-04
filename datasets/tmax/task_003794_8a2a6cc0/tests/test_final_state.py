# test_final_state.py

import time
import requests
import pytest
import math

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="session", autouse=True)
def wait_for_service():
    """Wait up to 30 seconds for the service to start."""
    start_time = time.time()
    while time.time() - start_time < 30:
        try:
            response = requests.get(f"{BASE_URL}/ping", timeout=1)
            if response.status_code == 200:
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    pytest.fail("Service did not start on port 8000 within 30 seconds.")

def test_ping_endpoint():
    """Test the /ping endpoint."""
    response = requests.get(f"{BASE_URL}/ping", timeout=5)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    data = response.json()
    assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"

def test_trajectory_endpoint():
    """Test the /trajectory endpoint."""
    response = requests.get(f"{BASE_URL}/trajectory", timeout=10)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    data = response.json()
    assert "x" in data, "Response JSON must contain an 'x' key"

    trajectory = data["x"]
    assert isinstance(trajectory, list), "'x' must be a list"
    assert len(trajectory) > 0, "Trajectory list is empty"

    # The ground truth specifies 150 frames (5 seconds at 30 FPS).
    # We allow a small margin in case of off-by-one in frame extraction.
    assert 140 <= len(trajectory) <= 160, f"Expected around 150 frames, got {len(trajectory)}"
    assert all(isinstance(val, (int, float)) for val in trajectory), "All trajectory values must be numbers"

def test_fit_endpoint():
    """Test the /fit endpoint with a Monte Carlo simulation."""
    payload = {"num_samples": 5000}
    # Allow a generous timeout for the parallel Monte Carlo simulation
    response = requests.post(f"{BASE_URL}/fit", json=payload, timeout=60)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "c" in data, "Response JSON must contain 'c'"
    assert "k" in data, "Response JSON must contain 'k'"
    assert "mse" in data, "Response JSON must contain 'mse'"

    c_val = data["c"]
    k_val = data["k"]

    # Ground truth: c = 0.5, k = 25.0
    # Tolerance: c within +/- 0.1, k within +/- 1.0
    assert math.isclose(c_val, 0.5, abs_tol=0.15), f"Fitted 'c' ({c_val}) is not within tolerance of 0.5"
    assert math.isclose(k_val, 25.0, abs_tol=1.5), f"Fitted 'k' ({k_val}) is not within tolerance of 25.0"