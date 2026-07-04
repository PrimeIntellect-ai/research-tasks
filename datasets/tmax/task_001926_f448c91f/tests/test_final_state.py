# test_final_state.py

import os
import socket
import requests
import math
import pytest

def test_redis_running():
    """Verify Redis is listening on port 6379."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 6379))
        assert result == 0, "Redis is not running or not listening on 127.0.0.1:6379"

def test_compute_engine_solve():
    """Verify the C++ compute engine applies Tikhonov regularization for near-singular matrices."""
    url = "http://127.0.0.1:8080/solve"
    payload = {
        "A": [[1.0, 1.0], [1.0, 1.0]],
        "b": [2.0, 2.0]
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to compute engine at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 from compute engine, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Compute engine did not return valid JSON. Response: {response.text}")

    assert "x" in data, f"Response from compute engine missing 'x' key. Response: {data}"

    x = data["x"]
    assert isinstance(x, list), f"Expected 'x' to be a list, got {type(x)}"
    assert len(x) == 2, f"Expected 2 elements in 'x', got {len(x)}"

    # Expected value is approximately 1.0 due to regularization (A + 1e-6*I)
    expected_val = 1.0
    for i, val in enumerate(x):
        assert isinstance(val, (int, float)), f"Element {i} is not a number: {val}"
        assert math.isclose(val, expected_val, rel_tol=1e-3, abs_tol=1e-3), \
            f"Element {i} of 'x' is {val}, expected approx {expected_val}. Regularization may not be applied correctly."

def test_flask_app_health():
    """Verify the Flask app is running and healthy."""
    url = "http://127.0.0.1:5000/health"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Flask app at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 from Flask app /health, got {response.status_code}"

def test_flask_app_simulate():
    """Verify the Flask app successfully processes a simulation request and returns valid numbers."""
    url = "http://127.0.0.1:5000/simulate"
    payload = {"size": 10, "anisotropy": 0.99999}

    try:
        response = requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Flask app at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 from Flask app /simulate, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Flask app did not return valid JSON. Response: {response.text}")

    assert "state" in data, f"Response missing 'state' key. Response: {data}"
    state = data["state"]

    assert isinstance(state, list), f"Expected 'state' to be a list, got {type(state)}"
    assert len(state) == 100, f"Expected 100 elements in state array, got {len(state)}"

    for i, val in enumerate(state):
        assert isinstance(val, (int, float)), f"Element {i} in state is not a number: {val}"
        assert not math.isnan(val), f"Found NaN at index {i} in state array"
        assert not math.isinf(val), f"Found Infinity at index {i} in state array"

def test_visualize_script_exists():
    """Verify the visualization script was created."""
    path = "/home/user/visualize.py"
    assert os.path.isfile(path), f"Visualize script {path} does not exist"

def test_heatmap_png_exists_and_valid():
    """Verify the heatmap PNG was generated and is a valid PNG file."""
    path = "/home/user/heatmap.png"
    assert os.path.isfile(path), f"Heatmap file {path} does not exist"

    # Check PNG magic number
    with open(path, "rb") as f:
        header = f.read(8)
        assert header == b'\x89PNG\r\n\x1a\n', f"File {path} is not a valid PNG image"