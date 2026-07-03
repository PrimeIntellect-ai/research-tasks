# test_final_state.py

import os
import requests
import pytest
import time

def test_c_source_exists():
    """Check if the C source file was created."""
    assert os.path.isfile("/home/user/mc_integral.c"), "/home/user/mc_integral.c does not exist."

def test_c_binary_exists_and_executable():
    """Check if the C binary was compiled and is executable."""
    binary_path = "/home/user/mc_integral"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_http_server_response():
    """Check if the HTTP server is running and returns the correct estimation."""
    url = "http://127.0.0.1:8080/simulate"
    params = {"samples": 5000000, "threads": 4}

    # Try connecting multiple times in case the server is slow to start
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            break
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                pytest.fail("Failed to connect to the HTTP server at 127.0.0.1:8080")
            time.sleep(1)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "result" in data, "JSON response does not contain the 'result' key."

    result = data["result"]
    assert isinstance(result, (int, float)), f"'result' must be a number, got {type(result)}"

    # The analytical integral is ~30.419. The test allows [30.3, 30.5]
    assert 30.3 <= result <= 30.5, f"Estimated integral {result} is out of expected bounds [30.3, 30.5]."