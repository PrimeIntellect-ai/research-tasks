# test_final_state.py

import os
import requests
import math
import pytest

def test_notebook_exists():
    """Check if the Jupyter Notebook was created."""
    assert os.path.isfile("/home/user/gbm_sim.ipynb"), "The Jupyter Notebook /home/user/gbm_sim.ipynb was not created."

def test_http_server_metrics():
    """Check if the HTTP server is running and returning the correct metrics."""
    url = "http://127.0.0.1:8080/metrics"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("The response from /metrics is not valid JSON.")

    expected_keys = {"S0", "mu", "sigma", "simulated_mean", "reference_mean", "difference"}
    assert set(data.keys()) == expected_keys, f"Expected keys {expected_keys}, got {set(data.keys())}"

    assert data["S0"] == 150, f"Expected S0 to be 150, got {data['S0']}"
    assert math.isclose(data["mu"], 0.08, abs_tol=0.001), f"Expected mu to be 0.08, got {data['mu']}"
    assert math.isclose(data["sigma"], 0.15, abs_tol=0.001), f"Expected sigma to be 0.15, got {data['sigma']}"

    assert math.isclose(data["simulated_mean"], 175.76, abs_tol=0.02), f"Expected simulated_mean to be ~175.76, got {data['simulated_mean']}"
    assert math.isclose(data["reference_mean"], 170.70, abs_tol=0.02), f"Expected reference_mean to be ~170.70, got {data['reference_mean']}"
    assert math.isclose(data["difference"], 5.06, abs_tol=0.02), f"Expected difference to be ~5.06, got {data['difference']}"