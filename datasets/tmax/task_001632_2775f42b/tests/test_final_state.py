# test_final_state.py
import os
import stat
import pytest
import requests
import time

def test_ode_sim_compiled():
    """Verify that the ode_sim binary has been compiled."""
    binary_path = "/app/spectral-ode-sim-1.0/ode_sim"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist. Did you fix the Makefile and compile?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_sim_results_generated():
    """Verify that the simulation results CSV was generated."""
    csv_path = "/home/user/sim_results.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist. Did you run the simulator?"
    assert os.path.getsize(csv_path) > 0, f"File {csv_path} is empty."

def test_analyze_and_serve_script_exists():
    """Verify that the analyze_and_serve.sh script exists."""
    script_path = "/home/user/analyze_and_serve.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_http_api_status():
    """Verify that the HTTP API is running and returns the correct JSON."""
    url = "http://127.0.0.1:8333/status"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}."

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type: application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    assert "peak_freq" in data, "JSON response missing 'peak_freq' key."
    assert "reference_match" in data, "JSON response missing 'reference_match' key."

    assert isinstance(data["peak_freq"], (int, float)), "'peak_freq' must be a number."
    assert isinstance(data["reference_match"], bool), "'reference_match' must be a boolean."

    # Check if the reference match is true (based on the setup, it should be)
    assert data["reference_match"] is True, "Expected reference_match to be true."