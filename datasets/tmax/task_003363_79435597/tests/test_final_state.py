# test_final_state.py

import os
import requests
import pytest
import time

def test_server_log_exists():
    log_path = "/home/user/server.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert "Server started on port 8080" in content, "Log file does not contain the expected startup message."

def test_http_server_sample_endpoint():
    url = "http://127.0.0.1:8080/sample"

    # Wait a bit in case the server is slow to start
    for _ in range(5):
        try:
            response = requests.get("http://127.0.0.1:8080/")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)

    payload = "10,20,-9999,30"
    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or send POST request: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    # The mean of 10, 20, 30 is 20.
    try:
        result = float(response.text.strip())
    except ValueError:
        pytest.fail(f"Expected a float response, got '{response.text}'")

    assert result == 20.0, f"Expected mean to be 20.0, got {result}"

def test_http_server_multiple_sentinels():
    url = "http://127.0.0.1:8080/sample"
    payload = "-9999,5,15,-9999,25,-9999"
    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or send POST request: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    # The mean of 5, 15, 25 is 15.
    try:
        result = float(response.text.strip())
    except ValueError:
        pytest.fail(f"Expected a float response, got '{response.text}'")

    assert result == 15.0, f"Expected mean to be 15.0, got {result}"