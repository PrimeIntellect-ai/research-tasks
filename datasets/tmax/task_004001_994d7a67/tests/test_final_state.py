# test_final_state.py

import os
import requests
import pytest

URL = "http://127.0.0.1:9000/process"
HEADERS = {"X-Auth-Token": "SecRes2024"}

def test_regression_files_exist():
    script_path = "/home/user/regression_test.sh"
    log_path = "/home/user/regression_results.log"

    assert os.path.exists(script_path), f"Regression test script {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    assert os.path.exists(log_path), f"Regression results log {log_path} is missing."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

def test_valid_request():
    payload = b"1.0\n2.0\n3.0\n"
    try:
        response = requests.post(URL, headers=HEADERS, data=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service or request timed out: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert "Mean: 2.000" in response.text and "Variance: 1.000" in response.text, \
        f"Unexpected response body: {response.text}"

def test_corrupted_request_recoverable():
    payload = b"1.0\n\x1B\x5B\x442.0\n3.0\n"
    try:
        response = requests.post(URL, headers=HEADERS, data=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service or request timed out: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert "Mean: 2.000" in response.text and "Variance: 1.000" in response.text, \
        f"Unexpected response body or failed to sanitize payload: {response.text}"

def test_unauthenticated_request():
    payload = b"1.0\n2.0\n3.0\n"
    try:
        response = requests.post(URL, data=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service or request timed out: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for unauthenticated request, got {response.status_code}"

    bad_headers = {"X-Auth-Token": "InvalidToken"}
    try:
        response_bad = requests.post(URL, headers=bad_headers, data=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the service or request timed out: {e}")

    assert response_bad.status_code == 401, f"Expected HTTP 401 for invalid token, got {response_bad.status_code}"