# test_final_state.py

import os
import subprocess
import json
import requests
import pytest

def test_mc_sim_compiled():
    """Verify the user compiled the C program to /home/user/mc_sim."""
    assert os.path.isfile("/home/user/mc_sim"), "The compiled executable /home/user/mc_sim does not exist."
    assert os.access("/home/user/mc_sim", os.X_OK), "/home/user/mc_sim is not executable."

def test_http_server_response():
    """Verify the HTTP server responds correctly to GET /data."""
    # First, compile the reference C code to get the exact pi value
    # We compile it ourselves to ensure it hasn't been tampered with and works properly
    compile_cmd = ["gcc", "-O3", "-fopenmp", "/home/user/mc_sim.c", "-o", "/tmp/mc_sim_ref"]
    subprocess.run(compile_cmd, check=True)

    # Run the reference executable with seed 8842 and 4 threads
    run_cmd = ["/tmp/mc_sim_ref", "8842", "4"]
    result = subprocess.run(run_cmd, capture_output=True, text=True, check=True)
    expected_pi_str = result.stdout.strip()

    try:
        expected_pi = float(expected_pi_str)
    except ValueError:
        pytest.fail(f"Could not parse pi value from reference implementation: {expected_pi_str}")

    # Make the HTTP request
    try:
        response = requests.get("http://127.0.0.1:8000/data", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at 127.0.0.1:8000/data: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Body: {response.text}")

    assert "seed" in data, "JSON response missing 'seed' field."
    assert "pi" in data, "JSON response missing 'pi' field."
    assert "fastest_thread_count" in data, "JSON response missing 'fastest_thread_count' field."

    assert data["seed"] == 8842, f"Expected seed 8842, got {data['seed']}"
    assert data["fastest_thread_count"] == 4, f"Expected fastest_thread_count 4, got {data['fastest_thread_count']}"

    # Compare pi values (allow small floating point differences if they parsed as float, or exact string match)
    # The C code prints 5 decimal places, so the float should be close.
    actual_pi = float(data["pi"])
    assert abs(actual_pi - expected_pi) < 1e-4, f"Expected pi value close to {expected_pi}, got {actual_pi}"