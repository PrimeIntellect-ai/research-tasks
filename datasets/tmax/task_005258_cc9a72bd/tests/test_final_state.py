# test_final_state.py

import os
import requests
import pytest
import json

def test_mc_sim_compiled():
    """Check if the C program was compiled."""
    executable_path = "/home/user/experiment/mc_sim"
    assert os.path.isfile(executable_path), f"Compiled executable {executable_path} not found."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_server_script_exists():
    """Check if the server script was created."""
    script_path = "/home/user/experiment/server.sh"
    assert os.path.isfile(script_path), f"Server script {script_path} not found."

def test_simulate_endpoint():
    """Check if the server is running and returns the correct simulation output."""
    url = "http://localhost:8080/simulate"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response body is not valid JSON. Response body: {response.text}")

    expected = {"steady_state": {"node0": 0.20, "node1": 0.32, "node2": 0.48}}
    assert data == expected, f"Expected {expected}, but got {data}"