# test_final_state.py

import os
import requests
import pytest
import math

COVARIANCE_FILE = "/home/user/covariance.txt"
BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer secret-token-99"}

def test_covariance_matrix():
    """Verify the covariance matrix is correctly computed and formatted."""
    assert os.path.exists(COVARIANCE_FILE), f"Covariance file not found at {COVARIANCE_FILE}"

    with open(COVARIANCE_FILE, 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) == 4, "Covariance matrix should have exactly 4 lines"

    expected_matrix = [
        [442.5000, 99.0000, 595.0000, 5875.0000],
        [99.0000, 22.4000, 134.0000, 1320.0000],
        [595.0000, 134.0000, 830.0000, 8150.0000],
        [5875.0000, 1320.0000, 8150.0000, 82500.0000]
    ]

    for i, line in enumerate(content):
        values = line.split(',')
        assert len(values) == 4, f"Line {i+1} does not have 4 values"
        for j, val in enumerate(values):
            assert val.count('.') == 1 and len(val.split('.')[1]) == 4, f"Value {val} is not formatted to 4 decimal places"
            assert math.isclose(float(val), expected_matrix[i][j], rel_tol=1e-4), f"Mismatch at row {i+1}, col {j+1}: expected {expected_matrix[i][j]}, got {val}"

def test_accuracy_endpoint():
    """Verify the /accuracy endpoint returns the correct accuracy."""
    try:
        response = requests.get(f"{BASE_URL}/accuracy", headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "accuracy" in data, "Response JSON missing 'accuracy' key"
    assert math.isclose(data["accuracy"], 0.8, rel_tol=1e-4), f"Expected accuracy 0.8, got {data['accuracy']}"

def test_predict_endpoint():
    """Verify the /predict endpoint returns correct probability and class."""
    payload = {"CPU": 40.0, "RAM": 4.0, "Disk": 10.0, "Network": 50.0}
    try:
        response = requests.post(f"{BASE_URL}/predict", headers=AUTH_HEADER, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "probability" in data, "Response JSON missing 'probability' key"
    assert "class" in data, "Response JSON missing 'class' key"

    # logit = 40*0.05 + 4*0.2 + 10*0.01 + 50*0.001 - 5.0 = 2.0 + 0.8 + 0.1 + 0.05 - 5.0 = -2.05
    # prob = 1 / (1 + exp(2.05)) ≈ 0.11405
    expected_prob = 1.0 / (1.0 + math.exp(2.05))

    assert math.isclose(data["probability"], expected_prob, abs_tol=1e-3), f"Expected probability ~{expected_prob}, got {data['probability']}"
    assert data["class"] == 0, f"Expected class 0, got {data['class']}"

def test_security_unauthorized():
    """Verify that requests without the correct authorization header are rejected."""
    endpoints = [
        ("GET", f"{BASE_URL}/accuracy", None),
        ("POST", f"{BASE_URL}/predict", {"CPU": 40.0, "RAM": 4.0, "Disk": 10.0, "Network": 50.0})
    ]

    for method, url, payload in endpoints:
        try:
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, json=payload, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to the server: {e}")

        assert response.status_code == 401, f"Expected 401 Unauthorized for {method} {url} without auth header, got {response.status_code}"