# test_final_state.py

import os
import json
import pytest
import requests
import math

def test_fitted_trajectory_json():
    path = "/home/user/fitted_trajectory.json"
    assert os.path.isfile(path), f"Missing fitted trajectory file: {path}"

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    # As the exact structure of the JSON is not strictly defined, we check if the file exists and is valid JSON.
    # The HTTP server test below will strictly validate the simulation correctness.
    assert isinstance(data, (dict, list)), "JSON should be a dictionary or a list."

def test_simulation_server_success():
    url = "http://127.0.0.1:8080/simulate?t=15"
    headers = {"Authorization": "Bearer sim-token-42"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the simulation server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Server did not return valid JSON. Response: {response.text}")

    assert "x" in data, "Response JSON missing 'x' key."
    assert "y" in data, "Response JSON missing 'y' key."

    expected_x = 40.0
    expected_y = 27.5

    assert math.isclose(float(data["x"]), expected_x, abs_tol=1.0), f"Expected x ~ {expected_x}, got {data['x']}"
    assert math.isclose(float(data["y"]), expected_y, abs_tol=1.0), f"Expected y ~ {expected_y}, got {data['y']}"

def test_simulation_server_auth():
    url = "http://127.0.0.1:8080/simulate?t=15"

    # Test without auth header
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code in (401, 403), f"Expected 401 or 403 for missing auth, got {response.status_code}"
    except requests.exceptions.RequestException:
        pass # Server might drop connection, which is also acceptable for missing auth

    # Test with wrong auth header
    headers = {"Authorization": "Bearer wrong-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        assert response.status_code in (401, 403), f"Expected 401 or 403 for invalid auth, got {response.status_code}"
    except requests.exceptions.RequestException:
        pass