# test_final_state.py
import os
import json
import math
import pytest
import requests

def test_extracted_path_file():
    filepath = "/home/user/extracted_path.json"
    assert os.path.exists(filepath), f"File not found: {filepath}"

    with open(filepath, 'r') as f:
        data = json.load(f)

    assert "x" in data, "Missing 'x' in extracted path"
    assert "y" in data, "Missing 'y' in extracted path"

    expected_x = [10, 30, 50, 70, 90]
    expected_y = [20, 25, 50, 25, 20]

    assert data["x"] == expected_x, f"Expected x coordinates {expected_x}, got {data['x']}"
    assert data["y"] == expected_y, f"Expected y coordinates {expected_y}, got {data['y']}"

def test_api_unauthorized():
    url = "http://127.0.0.1:9090/analyze"
    payload = {
        "auth": "BAD-TOKEN",
        "x_path": [1, 2, 3, 4, 5],
        "y_path": [1, 2, 3, 4, 5]
    }
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for bad auth, got {response.status_code}"

def test_api_normal_behavior():
    url = "http://127.0.0.1:9090/analyze"
    # Sending exactly the same coordinates as reference, should give 0 distance
    payload = {
        "auth": "LOG-ANALYSIS-TOK-55",
        "x_path": [10, 30, 50, 70, 90],
        "y_path": [20, 25, 50, 25, 20]
    }
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    data = response.json()
    assert "distance" in data, "Missing 'distance' in response"
    assert "is_anomaly" in data, "Missing 'is_anomaly' in response"

    assert math.isclose(data["distance"], 0.0, abs_tol=1e-4), f"Distance should be ~0.0, got {data['distance']}"
    assert data["is_anomaly"] is False, "Expected is_anomaly to be False for identical path"

def test_api_anomaly_behavior():
    url = "http://127.0.0.1:9090/analyze"
    # Sending completely different coordinates to trigger anomaly
    payload = {
        "auth": "LOG-ANALYSIS-TOK-55",
        "x_path": [90, 70, 50, 30, 10],
        "y_path": [50, 50, 50, 50, 50]
    }
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    data = response.json()
    assert "distance" in data, "Missing 'distance' in response"
    assert "is_anomaly" in data, "Missing 'is_anomaly' in response"

    assert data["distance"] > 0.5, f"Distance should be > 0.5, got {data['distance']}"
    assert data["is_anomaly"] is True, "Expected is_anomaly to be True for different path"