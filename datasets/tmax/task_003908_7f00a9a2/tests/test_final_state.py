# test_final_state.py
import os
import pytest
import requests
import time

def test_api_short_string():
    """Test the API with a short string."""
    url = "http://127.0.0.1:8080/process"
    payload = {"input": "hello"}
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API on 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    data = response.json()
    assert "result" in data, "Response JSON missing 'result' key"
    assert data["result"] == "HELLO", f"Expected 'HELLO', got '{data['result']}'"

def test_api_long_string():
    """Test the API with a string longer than 255 characters to verify the buffer overflow fix."""
    url = "http://127.0.0.1:8080/process"
    long_input = "a" * 300
    payload = {"input": long_input}
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API on 127.0.0.1:8080 with long string: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for long string, got {response.status_code}"

    data = response.json()
    assert "result" in data, "Response JSON missing 'result' key"
    expected_result = "A" * 300
    assert data["result"] == expected_result, f"Expected {expected_result}, got '{data['result']}'"

def test_e2e_script_exists_and_executable():
    """Check that the e2e test script was created and is executable."""
    script_path = "/app/test_e2e.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Bash script {script_path} is not executable."

def test_results_log_exists():
    """Check that the test results log was generated and contains status codes."""
    log_path = "/app/test_results.log"
    assert os.path.isfile(log_path), f"Test results log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "200" in content, "Test results log does not contain expected '200' HTTP status codes."