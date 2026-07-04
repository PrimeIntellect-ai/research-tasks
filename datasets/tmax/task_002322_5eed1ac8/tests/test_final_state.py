# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_regression_script_exists_and_executable():
    script_path = "/home/user/test.sh"
    assert os.path.isfile(script_path), f"Regression script {script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"Regression script {script_path} is not executable"

def test_regression_script_success():
    script_path = "/home/user/test.sh"
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Regression script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_api_transform_hello_world():
    url = "http://127.0.0.1:8080/transform"
    payload = "Hello World!"

    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to frontend API: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    expected_output = "1H1e2l1o1 1W1o1r1l1d1!"
    assert response.text == expected_output, f"Transformation incorrect. Expected '{expected_output}', got '{response.text}'"

def test_api_transform_aabbbc():
    url = "http://127.0.0.1:8080/transform"
    payload = "aabbbc"

    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to frontend API: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    expected_output = "2a3b1c"
    assert response.text == expected_output, f"Transformation incorrect. Expected '{expected_output}', got '{response.text}'"

def test_api_transform_sample_in():
    url = "http://127.0.0.1:8080/transform"

    with open("/app/sample_in.txt", "r") as f:
        payload = f.read()

    with open("/app/sample_out_expected.txt", "r") as f:
        expected_output = f.read()

    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to frontend API: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.text == expected_output, f"Transformation incorrect for sample_in.txt. Expected '{expected_output}', got '{response.text}'"