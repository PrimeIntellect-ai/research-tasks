# test_final_state.py

import os
import requests
import pytest

def expected_lcg(n):
    val = 42
    for _ in range(n):
        val = (val * 13 + 7) % 1000003
    return val

def test_regression_test_script_exists_and_executable():
    path = "/home/user/regression_test.py"
    assert os.path.isfile(path), f"Regression test script {path} does not exist."
    assert os.access(path, os.X_OK), f"Regression test script {path} is not executable."

@pytest.mark.parametrize("n", [0, 1, 10, 50, 100, 1000])
def test_service_responses(n):
    url = f"http://127.0.0.1:8080/calc?n={n}"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code} for n={n}."

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response text: {response.text}")

    assert "result" in data, f"Response JSON missing 'result' key. Got: {data}"

    expected_value = expected_lcg(n)
    assert data["result"] == expected_value, f"Expected result {expected_value} for n={n}, got {data['result']}."