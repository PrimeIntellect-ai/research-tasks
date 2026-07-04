# test_final_state.py

import os
import json
import math
import pytest
import requests

def test_tracking_json():
    tracking_file = "/home/user/tracking.json"
    assert os.path.isfile(tracking_file), f"Tracking file {tracking_file} does not exist."

    with open(tracking_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {tracking_file} is not valid JSON.")

    assert "dropped_sensor" in data, "Missing 'dropped_sensor' in tracking.json"
    assert data["dropped_sensor"] == "sensor_B", "Incorrect 'dropped_sensor'. Expected 'sensor_B'."

    assert "covariance_determinant" in data, "Missing 'covariance_determinant' in tracking.json"

    # The covariance matrix of A, C, D using n-1 degrees of freedom has a determinant of 1.7225
    expected_det = 1.7225
    actual_det = data["covariance_determinant"]
    assert isinstance(actual_det, (int, float)), "'covariance_determinant' must be a number."
    assert math.isclose(actual_det, expected_det, rel_tol=1e-3, abs_tol=1e-4), \
        f"Incorrect covariance determinant. Expected approx {expected_det}, got {actual_det}."

def test_api_unauthorized():
    url = "http://127.0.0.1:8000/infer"
    payload = {"sensor_A": 1.0, "sensor_C": 0.5, "sensor_D": 1.1}

    # No auth
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

    # Wrong auth
    headers = {"Authorization": "Bearer wrong_token"}
    response = requests.post(url, json=payload, headers=headers, timeout=2)
    assert response.status_code == 401, f"Expected 401 Unauthorized with wrong token, got {response.status_code}"

def test_api_authorized_and_logic():
    url = "http://127.0.0.1:8000/infer"
    payload = {"sensor_A": 1.0, "sensor_C": 0.5, "sensor_D": 1.1}
    headers = {"Authorization": "Bearer lab_auth_token_88"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "posterior_probability" in data, "Missing 'posterior_probability' in response."

    # 1.0 + 0.5 + 1.1 = 2.6
    # 1 / (1 + exp(-2.6)) = 0.9308615796412287
    expected_prob = 1.0 / (1.0 + math.exp(-2.6))
    actual_prob = data["posterior_probability"]

    assert isinstance(actual_prob, (int, float)), "'posterior_probability' must be a number."
    assert math.isclose(actual_prob, expected_prob, rel_tol=1e-5, abs_tol=1e-5), \
        f"Incorrect posterior probability. Expected approx {expected_prob}, got {actual_prob}."