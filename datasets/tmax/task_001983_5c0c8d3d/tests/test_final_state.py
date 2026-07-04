# test_final_state.py

import os
import requests
import pytest

def test_sim_py_fixed():
    """Check that the deliberate perturbation is removed from sim.py."""
    sim_path = "/app/vendored_bio_sim/sim.py"
    assert os.path.isfile(sim_path), f"{sim_path} is missing."

    with open(sim_path, "r") as f:
        content = f.read()

    assert "first_step=1000.0" not in content, "The deliberate perturbation 'first_step=1000.0' is still present in sim.py."

def test_server_unauthorized():
    """Check that the server returns 401 when the Authorization header is missing."""
    url = "http://127.0.0.1:8888/simulate"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for missing auth, but got {response.status_code}."

def test_server_invalid_auth():
    """Check that the server returns 401 when the Authorization header is invalid."""
    url = "http://127.0.0.1:8888/simulate"
    headers = {"Authorization": "Bearer invalid-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for invalid auth, but got {response.status_code}."

def test_server_success():
    """Check that the server returns 200 and the correct JSON payload on success."""
    url = "http://127.0.0.1:8888/simulate"
    headers = {"Authorization": "Bearer sim-token-42"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200 for valid auth, but got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Server did not return valid JSON. Response body: {response.text}")

    assert "distance" in data, "The JSON response is missing the 'distance' key."
    distance = data["distance"]
    assert isinstance(distance, float), f"Expected 'distance' to be a float, but got {type(distance).__name__}."
    assert distance > 0.0, f"Expected 'distance' to be greater than 0.0, but got {distance}."