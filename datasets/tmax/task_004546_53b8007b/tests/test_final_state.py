# test_final_state.py

import os
import subprocess
import time
import requests
import pytest
import math

SERVICE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer sim-perf-token-2024"}

@pytest.fixture(scope="module", autouse=True)
def start_service():
    """Start the service and yield, then kill it."""
    script_path = "/home/user/start_service.sh"
    assert os.path.isfile(script_path), f"Startup script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Startup script is not executable: {script_path}"

    # Start the service
    proc = subprocess.Popen(["/bin/bash", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for service to be available
    service_up = False
    for _ in range(30):
        try:
            requests.get(SERVICE_URL, timeout=0.5)
            # Even if it returns 404 or 401, the connection was accepted
            service_up = True
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)

    if not service_up:
        proc.terminate()
        pytest.fail("Service did not start on 127.0.0.1:8080 within 15 seconds.")

    yield

    # Teardown
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()

def test_auth_required():
    """Test that endpoints require the correct Bearer token."""
    resp = requests.get(f"{SERVICE_URL}/simulate?start_price=100")
    assert resp.status_code in [401, 403], f"Expected 401/403 without auth, got {resp.status_code}"

    resp = requests.get(f"{SERVICE_URL}/regression")
    assert resp.status_code in [401, 403], f"Expected 401/403 without auth, got {resp.status_code}"

def test_simulate_endpoint_deterministic():
    """Test that the simulate endpoint returns deterministic results."""
    results = set()
    for _ in range(5):
        resp = requests.get(f"{SERVICE_URL}/simulate?start_price=100", headers=AUTH_HEADER)
        assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Body: {resp.text}"
        try:
            val = float(resp.text.strip())
            results.add(val)
        except ValueError:
            pytest.fail(f"Could not parse response as float: {resp.text}")

    assert len(results) == 1, f"Simulation is not deterministic, got multiple results for start_price=100: {results}"

def test_regression_endpoint():
    """Test the regression endpoint and verify it matches the simulation results."""
    # Gather simulation results
    prices = []
    for x in range(100, 200, 10):
        resp = requests.get(f"{SERVICE_URL}/simulate?start_price={x}", headers=AUTH_HEADER)
        assert resp.status_code == 200
        prices.append((x, float(resp.text.strip())))

    # Calculate expected regression
    n = len(prices)
    sum_x = sum(x for x, y in prices)
    sum_y = sum(y for x, y in prices)
    sum_xy = sum(x * y for x, y in prices)
    sum_x2 = sum(x * x for x, y in prices)

    denominator = (n * sum_x2 - sum_x ** 2)
    expected_m = (n * sum_xy - sum_x * sum_y) / denominator
    expected_c = (sum_y - expected_m * sum_x) / n

    # Get regression from endpoint
    resp = requests.get(f"{SERVICE_URL}/regression", headers=AUTH_HEADER)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Body: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Could not parse response as JSON: {resp.text}")

    assert "slope" in data, "Missing 'slope' in regression response"
    assert "intercept" in data, "Missing 'intercept' in regression response"

    actual_m = float(data["slope"])
    actual_c = float(data["intercept"])

    assert math.isclose(actual_m, expected_m, rel_tol=1e-3), f"Slope mismatch: expected {expected_m}, got {actual_m}"
    assert math.isclose(actual_c, expected_c, rel_tol=1e-3), f"Intercept mismatch: expected {expected_c}, got {actual_c}"