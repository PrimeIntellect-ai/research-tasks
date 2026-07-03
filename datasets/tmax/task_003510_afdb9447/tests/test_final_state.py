# test_final_state.py

import os
import math
import requests
import pytest

def test_libtinyml_compiled():
    lib_path = "/app/tinyml/libtinyml.a"
    assert os.path.isfile(lib_path), f"Expected compiled library at {lib_path} does not exist. Did you fix the Makefile and compile it?"

def test_unauthorized_request():
    url = "http://127.0.0.1:8080/infer"
    payload = {"features": [2.0, 4.0, -9999.0, 100.0, 6.0]}

    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected status code 401 for unauthorized request, got {response.status_code}"

def test_inference_logic():
    url = "http://127.0.0.1:8080/infer"
    headers = {"Authorization": "Bearer super-secret-ds-token"}
    payload = {"features": [2.0, 4.0, -9999.0, 100.0, 6.0]}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "cleaned" in data, "Response JSON missing 'cleaned' key"
    assert "prediction" in data, "Response JSON missing 'prediction' key"

    expected_cleaned = [2.0, 4.0, 28.0, 100.0, 6.0]
    actual_cleaned = data["cleaned"]
    assert len(actual_cleaned) == 5, f"Expected cleaned array of length 5, got {len(actual_cleaned)}"

    for i, (exp, act) in enumerate(zip(expected_cleaned, actual_cleaned)):
        assert math.isclose(exp, act, rel_tol=1e-4, abs_tol=1e-4), f"Mismatch in cleaned array at index {i}: expected {exp}, got {act}"

    expected_prediction = 90.2
    actual_prediction = data["prediction"]
    assert math.isclose(expected_prediction, actual_prediction, rel_tol=1e-4, abs_tol=1e-4), f"Expected prediction {expected_prediction}, got {actual_prediction}"

def test_inference_logic_all_valid():
    url = "http://127.0.0.1:8080/infer"
    headers = {"Authorization": "Bearer super-secret-ds-token"}
    payload = {"features": [1.0, 2.0, 3.0, 4.0, 5.0]}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    data = response.json()

    expected_cleaned = [1.0, 2.0, 3.0, 4.0, 5.0]
    actual_cleaned = data.get("cleaned", [])

    for i, (exp, act) in enumerate(zip(expected_cleaned, actual_cleaned)):
        assert math.isclose(exp, act, rel_tol=1e-4, abs_tol=1e-4), f"Mismatch in cleaned array at index {i}: expected {exp}, got {act}"

    # Weights: [0.2, 0.8, -0.5, 1.0, 0.1]
    # Dot product: 0.2 + 1.6 - 1.5 + 4.0 + 0.5 = 4.8
    expected_prediction = 4.8
    actual_prediction = data.get("prediction", 0.0)
    assert math.isclose(expected_prediction, actual_prediction, rel_tol=1e-4, abs_tol=1e-4), f"Expected prediction {expected_prediction}, got {actual_prediction}"