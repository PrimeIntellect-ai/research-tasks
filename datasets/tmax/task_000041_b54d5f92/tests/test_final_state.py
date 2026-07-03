# test_final_state.py

import os
import math
import subprocess
import requests
import pytest

def test_go_test_passes():
    """Verify that the standard Go test passes in /home/user/sim_server."""
    sim_dir = "/home/user/sim_server"
    assert os.path.isdir(sim_dir), f"Expected directory {sim_dir} does not exist."

    try:
        result = subprocess.run(
            ["go", "test"],
            cwd=sim_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
    except FileNotFoundError:
        pytest.fail("Go toolchain not found. Is Go installed?")
    except subprocess.TimeoutExpired:
        pytest.fail("go test command timed out.")

    assert result.returncode == 0, f"'go test' failed with output:\n{result.stdout}\n{result.stderr}"

def test_http_server_response():
    """Verify that the HTTP server responds correctly on port 9090."""
    url = "http://127.0.0.1:9090/solve"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "max_amplitude" in data, "Response JSON missing 'max_amplitude' field."
    assert "solution" in data, "Response JSON missing 'solution' field."

    # Check max_amplitude
    expected_amplitude = 15000.0
    assert math.isclose(data["max_amplitude"], expected_amplitude, rel_tol=1e-5), \
        f"Expected max_amplitude to be {expected_amplitude}, got {data['max_amplitude']}"

    # Check solution
    expected_solution = [4620.535714285715, 3482.1428571428573, 1808.0357142857142]
    actual_solution = data["solution"]

    assert isinstance(actual_solution, list), "'solution' must be a list."
    assert len(actual_solution) == 3, f"Expected 'solution' to have 3 elements, got {len(actual_solution)}"

    for i, (actual, expected) in enumerate(zip(actual_solution, expected_solution)):
        assert math.isclose(actual, expected, abs_tol=0.01), \
            f"Solution element {i} incorrect. Expected approx {expected}, got {actual}"