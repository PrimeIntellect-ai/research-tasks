# test_final_state.py
import os
import subprocess
import requests
import math
import pytest

def test_solver_binary_exists_and_linked_openmp():
    binary_path = '/app/ridge_solver/solver'
    assert os.path.isfile(binary_path), "The compiled binary 'solver' is missing in /app/ridge_solver"
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable"

    # Check if compiled with OpenMP
    try:
        ldd_output = subprocess.check_output(['ldd', binary_path], text=True)
        assert 'libgomp' in ldd_output or 'libomp' in ldd_output, "The binary does not appear to be linked with OpenMP (e.g. libgomp). Did you compile with OpenMP support?"
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run ldd on the compiled binary to check for OpenMP linkage.")

def test_service_responses():
    url = "http://127.0.0.1:8080/fit"

    # Test case: near-singular / singular matrix
    # Points: (1.0, 2.0) and (1.0, 2.0)
    # sum_x2 = 2, sum_x = 2, sum_y = 4, sum_xy = 4, n = 2
    # lambda = 1.0
    # a = 3, b = 2, c = 2, d = 3
    # det = 5
    # inv_a = 0.6, inv_b = -0.4, inv_c = -0.4, inv_d = 0.6
    # w1 = 0.6*4 - 0.4*4 = 0.8
    # w0 = -0.4*4 + 0.6*4 = 0.8

    payload = {
        "lambda": 1.0,
        "points": [
            {"x": 1.0, "y": 2.0},
            {"x": 1.0, "y": 2.0}
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the server at 127.0.0.1:8080. Is the server running?")
    except requests.exceptions.Timeout:
        pytest.fail("Request to the server timed out.")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "w1" in data and "w0" in data, f"Response JSON missing 'w1' or 'w0' keys: {data}"

    w1 = data["w1"]
    w0 = data["w0"]

    # Check for NaN
    assert not math.isnan(w1), "w1 is NaN. The regularization parameter lambda was not correctly applied to prevent division by zero."
    assert not math.isnan(w0), "w0 is NaN. The regularization parameter lambda was not correctly applied to prevent division by zero."

    # Check exact expected values (with small tolerance for float arithmetic)
    assert math.isclose(w1, 0.8, rel_tol=1e-4), f"Expected w1 ≈ 0.8, got {w1}. Ensure lambda is added to both a and d."
    assert math.isclose(w0, 0.8, rel_tol=1e-4), f"Expected w0 ≈ 0.8, got {w0}. Ensure lambda is added to both a and d."