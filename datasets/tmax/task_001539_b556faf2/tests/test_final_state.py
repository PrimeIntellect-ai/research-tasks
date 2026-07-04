# test_final_state.py

import os
import math
import requests
import pytest

def expected_displacement(t, x0, v0):
    omega_n = 2.0
    zeta = 0.1
    omega_d = omega_n * math.sqrt(1 - zeta**2)
    C1 = x0
    C2 = (v0 + zeta * omega_n * x0) / omega_d
    return math.exp(-zeta * omega_n * t) * (C1 * math.cos(omega_d * t) + C2 * math.sin(omega_d * t))

def test_ode_solver_files_exist():
    c_file = "/home/user/ode_solver.c"
    exe_file = "/home/user/ode_solver"

    assert os.path.exists(c_file), f"C source file {c_file} is missing."
    assert os.path.exists(exe_file), f"Executable {exe_file} is missing."
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/predict"
    payload = {"t": 3.5, "x0": 100.0, "v0": -50.0}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_api_predict():
    url = "http://127.0.0.1:8080/predict"
    headers = {"Authorization": "Bearer ODE-FIT-2024"}

    test_cases = [
        {"t": 3.5, "x0": 100.0, "v0": -50.0},
        {"t": 1.0, "x0": 50.0, "v0": 0.0},
        {"t": 5.0, "x0": -50.0, "v0": 20.0}
    ]

    for case in test_cases:
        try:
            response = requests.post(url, json=case, headers=headers, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to API server: {e}")

        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {response.text}")

        assert "x" in data, f"Response JSON missing 'x' key: {data}"

        predicted_x = data["x"]
        expected_x = expected_displacement(case["t"], case["x0"], case["v0"])

        tolerance = max(0.05 * abs(expected_x), 1e-3)
        assert math.isclose(predicted_x, expected_x, abs_tol=tolerance), \
            f"For parameters {case}, expected x ≈ {expected_x:.4f}, but got {predicted_x:.4f} (tolerance: +/- 5%)"