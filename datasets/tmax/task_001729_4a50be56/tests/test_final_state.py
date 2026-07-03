# test_final_state.py
import os
import requests
import pytest

def test_binary_compiled():
    binary_path = "/app/nano_ode_aligner-2.1.0/bin/nano_align"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def test_makefile_fixed():
    makefile_path = "/app/nano_ode_aligner-2.1.0/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-fopenmp" in content, "Makefile was not fixed to include -fopenmp"

def test_solver_fixed():
    solver_path = "/app/nano_ode_aligner-2.1.0/src/solver.c"
    assert os.path.isfile(solver_path), f"solver.c not found at {solver_path}"
    with open(solver_path, "r") as f:
        content = f.read()
    assert "dt = dt * 1.5;" not in content, "solver.c still contains the buggy step size adaptation logic"

def test_service_analyze_valid_request():
    url = "http://127.0.0.1:9090/analyze"
    headers = {"X-Nano-Auth": "spectro-secure-token", "Content-Type": "application/json"}
    payload = {"signal": [1.12, 1.15, 0.98, 0.85, 1.01, 1.05, 0.99]}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service or request timed out: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    assert "variant" in data, "Response JSON missing 'variant' key"
    assert "log_ratio" in data, "Response JSON missing 'log_ratio' key"

    assert isinstance(data["variant"], bool), f"'variant' must be a boolean, got {type(data['variant'])}"
    assert isinstance(data["log_ratio"], (float, int)), f"'log_ratio' must be a float, got {type(data['log_ratio'])}"

def test_service_auth_required():
    url = "http://127.0.0.1:9090/analyze"
    headers = {"Content-Type": "application/json"}
    payload = {"signal": [1.12, 1.15, 0.98, 0.85, 1.01, 1.05, 0.99]}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    # Standard HTTP status codes for missing/invalid authentication are 401 or 403
    assert response.status_code in (401, 403), f"Expected 401 or 403 for missing auth header, got {response.status_code}"