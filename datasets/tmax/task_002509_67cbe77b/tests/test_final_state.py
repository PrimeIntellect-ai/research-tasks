# test_final_state.py

import os
import pytest
import requests
import math

def test_compiled_executable_exists():
    """Verify that the compiled integrator executable exists."""
    executable_path = "/home/user/integrator"
    assert os.path.exists(executable_path), f"Compiled executable missing: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File is not executable: {executable_path}"

def test_analyze_script_exists():
    """Verify that the analyze.sh script exists."""
    script_path = "/home/user/analyze.sh"
    assert os.path.exists(script_path), f"Analyze script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_simulate_endpoint_unauthorized():
    """Verify that the /simulate endpoint rejects unauthorized requests with 401."""
    url = "http://127.0.0.1:8080/simulate"
    payload = {"duration": 50.0}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_simulate_endpoint_authorized_and_correct():
    """Verify that the /simulate endpoint works correctly with valid auth and payload."""
    url = "http://127.0.0.1:8080/simulate"
    payload = {"duration": 50.0}
    headers = {"Authorization": "Bearer perf-eng-token-2024"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "h_max" in data, "Response JSON missing 'h_max' field"
    assert "dominant_frequency" in data, "Response JSON missing 'dominant_frequency' field"

    h_max = data["h_max"]
    dominant_frequency = data["dominant_frequency"]

    assert isinstance(h_max, (int, float)), "h_max must be a number"
    assert isinstance(dominant_frequency, (int, float)), "dominant_frequency must be a number"

    # Check constraints
    assert h_max <= 0.05, f"h_max should be <= 0.05 to demonstrate stable integration, got {h_max}"
    assert math.isclose(dominant_frequency, 2.5, abs_tol=0.2), f"dominant_frequency should be close to 2.5, got {dominant_frequency}"