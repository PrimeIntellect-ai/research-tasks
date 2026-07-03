# test_final_state.py

import os
import requests
import pytest
import math

BASE_URL = "http://127.0.0.1:8080"

def test_c_file_exists():
    assert os.path.exists("/home/user/model.c"), "C program /home/user/model.c is missing."

def test_api_trajectory():
    try:
        response = requests.get(f"{BASE_URL}/api/trajectory", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/api/trajectory: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "Expected a JSON array for trajectory"
    assert len(data) == 100, f"Expected 100 frames, got {len(data)}"

    first_frame = data[0]
    assert "frame" in first_frame and first_frame["frame"] == 0, "First frame should have frame=0"
    assert "x" in first_frame and "y" in first_frame, "Trajectory objects must have 'x' and 'y' keys"
    assert math.isclose(first_frame["x"], 100.0, abs_tol=2.0), f"Expected x[0] ~ 100.0, got {first_frame['x']}"
    assert math.isclose(first_frame["y"], 100.0, abs_tol=2.0), f"Expected y[0] ~ 100.0, got {first_frame['y']}"

def test_api_parameters():
    try:
        response = requests.get(f"{BASE_URL}/api/parameters", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/api/parameters: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()

    for key in ["vx", "x0", "y0", "vy", "A", "omega"]:
        assert key in data, f"Missing key '{key}' in parameters response"

    assert math.isclose(data["A"], 10.0, abs_tol=1.5), f"Expected A ~ 10.0, got {data['A']}"
    assert math.isclose(data["omega"], 0.1, abs_tol=0.05), f"Expected omega ~ 0.1, got {data['omega']}"

def test_api_stats():
    try:
        response = requests.get(f"{BASE_URL}/api/stats", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/api/stats: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    data = response.json()

    assert "f_statistic" in data, "Missing 'f_statistic' in stats response"
    assert "better_model" in data, "Missing 'better_model' in stats response"
    assert data["better_model"] == "nonlinear", f"Expected better_model to be 'nonlinear', got {data['better_model']}"