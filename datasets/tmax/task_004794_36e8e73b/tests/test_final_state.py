# test_final_state.py

import os
import math
import pytest
import requests
import json

def test_server_ready_file():
    """Check that the agent signaled the server is ready."""
    assert os.path.exists("/tmp/server_ready"), "The file /tmp/server_ready was not created."

def test_auth_required():
    """Check that the API requires the correct authorization header."""
    url = "http://127.0.0.1:9000/metric"
    payload = {"index": 0, "candidate": [0.1] * 10}

    # No auth header
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}"

def test_kl_divergence_computation():
    """Check that the KL divergence is computed correctly for index 0."""
    try:
        import h5py
        import numpy as np
    except ImportError:
        pytest.fail("h5py and numpy are required for the test but are not installed.")

    # Read the actual truth data
    try:
        with h5py.File('/app/raw_data.h5', 'r') as f:
            matrix_0 = f['covariances'][0]
    except Exception as e:
        pytest.fail(f"Failed to read /app/raw_data.h5: {e}")

    # Compute expected P from the oracle logic (softmax of diagonal)
    diag_0 = np.diag(matrix_0)
    max_val = np.max(diag_0)
    exp_diag = np.exp(diag_0 - max_val)
    P = exp_diag / np.sum(exp_diag)

    Q = np.array([0.1] * 10)

    # Compute KL divergence
    # The instructions mentioned adding 1e-9 if necessary, so we accept both strict and smoothed versions
    kl_strict = np.sum(P * np.log(P / Q))
    kl_smoothed = np.sum(P * np.log((P + 1e-9) / (Q + 1e-9)))

    url = "http://127.0.0.1:9000/metric"
    headers = {"Authorization": "Bearer secret-ml-token-99"}
    payload = {"index": 0, "candidate": [0.1] * 10}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Server did not return valid JSON. Response: {response.text}")

    assert "distance" in data, f"Response JSON missing 'distance' key. Got: {data}"

    distance = data["distance"]
    assert isinstance(distance, (int, float)), "Distance must be a number."

    is_close_strict = math.isclose(distance, kl_strict, rel_tol=1e-3, abs_tol=1e-4)
    is_close_smoothed = math.isclose(distance, kl_smoothed, rel_tol=1e-3, abs_tol=1e-4)

    assert is_close_strict or is_close_smoothed, \
        f"Computed KL divergence {distance} does not match expected {kl_strict:.5f} (or smoothed {kl_smoothed:.5f})"