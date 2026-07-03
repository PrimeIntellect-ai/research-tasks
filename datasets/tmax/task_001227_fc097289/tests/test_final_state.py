# test_final_state.py

import os
import requests
import pytest

SERVICE_URL = "http://127.0.0.1:8000/profile"

def test_unauthorized_request():
    """Test that an invalid token returns a 401 Unauthorized status."""
    payload = {
        "token": "bad-token",
        "start_N": 8,
        "target_error": 0.05
    }
    try:
        response = requests.post(SERVICE_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for bad token, got {response.status_code}"

def test_valid_request_and_convergence():
    """Test a valid request, verify the response schema, and check convergence logic."""
    payload = {
        "token": "pde-admin-token",
        "start_N": 8,
        "target_error": 0.02
    }

    # Ensure plot does not exist before or we just check it after
    if os.path.exists("/home/user/profile_plot.png"):
        os.remove("/home/user/profile_plot.png")

    try:
        response = requests.post(SERVICE_URL, json=payload, timeout=30)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "converged_N" in data, "Missing 'converged_N' in response"
    assert "errors" in data, "Missing 'errors' in response"
    assert "execution_times" in data, "Missing 'execution_times' in response"

    converged_N = data["converged_N"]
    errors = data["errors"]
    execution_times = data["execution_times"]

    assert isinstance(converged_N, int), "'converged_N' must be an integer"
    assert isinstance(errors, list) and all(isinstance(e, (int, float)) for e in errors), "'errors' must be a list of floats"
    assert isinstance(execution_times, list) and all(isinstance(t, (int, float)) for t in execution_times), "'execution_times' must be a list of floats"

    assert len(errors) > 0, "Errors list is empty"
    assert len(errors) == len(execution_times), "Length of errors and execution_times must match"

    # Check convergence logic
    assert errors[-1] <= 0.02, f"Last error {errors[-1]} is not <= target_error 0.02"
    if len(errors) > 1:
        assert errors[-2] > 0.02, f"Second to last error {errors[-2]} should be > target_error 0.02"

    expected_N = payload["start_N"] * (2 ** (len(errors) - 1))
    assert converged_N == expected_N, f"Expected converged_N to be {expected_N}, got {converged_N}"

def test_plot_generated():
    """Check if the plot was generated at the correct path."""
    plot_path = "/home/user/profile_plot.png"
    assert os.path.isfile(plot_path), f"Plot file {plot_path} was not generated."

def test_c_code_fixes():
    """Check if the C code and Makefile were fixed properly."""
    with open("/app/pde_solver/solver.c", "r") as f:
        c_content = f.read()
    assert "#define IDX(i, j, N) (i * N + j)" in c_content.replace(" ", ""), "The IDX macro in solver.c was not fixed correctly."

    with open("/app/pde_solver/Makefile", "r") as f:
        makefile_content = f.read()
    assert "-lm" in makefile_content, "The Makefile does not contain the required '-lm' flag."