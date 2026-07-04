# test_final_state.py

import json
import math
import os
import time
import requests
import pytest

def test_plot_exists():
    assert os.path.exists("/home/user/fit_plot.png"), "Visualization plot /home/user/fit_plot.png does not exist."

def test_server_ready_file():
    assert os.path.exists("/home/user/server_ready.txt"), "The marker file /home/user/server_ready.txt was not created."

def test_api_unauthorized():
    try:
        response = requests.get("http://127.0.0.1:8000/params", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for request without auth, got {response.status_code}"

def test_api_params():
    # Read the expected parameters from the setup script's output
    assert os.path.exists("/tmp/expected_params.json"), "Expected parameters file not found. Setup might be broken."
    with open("/tmp/expected_params.json", "r") as f:
        expected = json.load(f)

    headers = {"Authorization": "Bearer perf-token-2024"}
    try:
        response = requests.get("http://127.0.0.1:8000/params", headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON from response: {response.text}")

    assert "k" in data, "Missing 'k' parameter in response"
    assert "theta" in data, "Missing 'theta' parameter in response"

    # Allow some tolerance due to different root finding implementations
    assert math.isclose(data["k"], expected["k"], rel_tol=1e-2), f"Estimated 'k' ({data['k']}) does not match expected ({expected['k']})"
    assert math.isclose(data["theta"], expected["theta"], rel_tol=1e-2), f"Estimated 'theta' ({data['theta']}) does not match expected ({expected['theta']})"

def test_api_pdf():
    # Read the expected parameters to compute the expected PDF
    with open("/tmp/expected_params.json", "r") as f:
        expected = json.load(f)

    k = expected["k"]
    theta = expected["theta"]
    x = 15.0

    # Compute Gamma PDF: f(x; k, theta) = x^(k-1) * e^(-x/theta) / (theta^k * Gamma(k))
    expected_pdf = (x**(k-1) * math.exp(-x/theta)) / (theta**k * math.gamma(k))

    headers = {"Authorization": "Bearer perf-token-2024"}
    try:
        response = requests.get(f"http://127.0.0.1:8000/pdf?x={x}", headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON from response: {response.text}")

    assert "pdf" in data, "Missing 'pdf' key in response"
    assert math.isclose(data["pdf"], expected_pdf, rel_tol=1e-2), f"Calculated 'pdf' ({data['pdf']}) does not match expected ({expected_pdf})"