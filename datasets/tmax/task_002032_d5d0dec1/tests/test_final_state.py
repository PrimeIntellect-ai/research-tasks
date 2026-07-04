# test_final_state.py

import pytest
import requests
import json
import math

URL = "http://127.0.0.1:5050/process"
HEADERS = {"X-Pipeline-Token": "alpha-etl-883"}

def test_service_running_and_unauthorized_rejected():
    """Test that the service is running and rejects requests without the correct token."""
    try:
        response = requests.post(URL, data="1.0,2.0,3.0,4.0,5.0", timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not listening on 127.0.0.1:5050")

    assert response.status_code in [401, 403], f"Expected 401 or 403 for missing token, got {response.status_code}"

def test_service_wrong_token_rejected():
    """Test that the service rejects requests with an incorrect token."""
    try:
        response = requests.post(URL, headers={"X-Pipeline-Token": "wrong-token"}, data="1.0,2.0,3.0,4.0,5.0", timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not listening on 127.0.0.1:5050")

    assert response.status_code in [401, 403], f"Expected 401 or 403 for wrong token, got {response.status_code}"

def test_service_process_valid_data():
    """Test the /process endpoint with valid data and correct imputation."""
    payload = "1.5,?,5.5,?,9.0"
    try:
        response = requests.post(URL, headers=HEADERS, data=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not listening on 127.0.0.1:5050")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "imputed" in data, "Response JSON missing 'imputed' key"
    assert "score" in data, "Response JSON missing 'score' key"

    expected_imputed = [1.5, 3.5, 5.5, 5.5, 9.0]
    actual_imputed = data["imputed"]

    assert isinstance(actual_imputed, list), "'imputed' should be a list"
    assert len(actual_imputed) == 5, f"Expected 5 imputed values, got {len(actual_imputed)}"

    for expected, actual in zip(expected_imputed, actual_imputed):
        assert math.isclose(expected, actual, rel_tol=1e-5), f"Imputed values mismatch. Expected {expected_imputed}, got {actual_imputed}"

    expected_score = 6.24
    actual_score = data["score"]
    assert isinstance(actual_score, (int, float)), "'score' should be a number"
    assert math.isclose(expected_score, actual_score, rel_tol=1e-2), f"Score mismatch. Expected {expected_score}, got {actual_score}"

def test_service_process_no_missing_data():
    """Test the /process endpoint with no missing data."""
    payload = "2.0,4.0,6.0,8.0,10.0"
    try:
        response = requests.post(URL, headers=HEADERS, data=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not listening on 127.0.0.1:5050")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    data = response.json()

    expected_imputed = [2.0, 4.0, 6.0, 8.0, 10.0]
    actual_imputed = data["imputed"]

    for expected, actual in zip(expected_imputed, actual_imputed):
        assert math.isclose(expected, actual, rel_tol=1e-5), f"Imputed values mismatch. Expected {expected_imputed}, got {actual_imputed}"

    # Calculate expected score: sqrt((2/2)^2 + (4/2)^2 + (6/2)^2 + (8/2)^2 + (10/2)^2)
    # = sqrt(1 + 4 + 9 + 16 + 25) = sqrt(55) = 7.416...
    expected_score = 7.42
    actual_score = data["score"]
    assert math.isclose(expected_score, actual_score, rel_tol=1e-2), f"Score mismatch. Expected {expected_score}, got {actual_score}"