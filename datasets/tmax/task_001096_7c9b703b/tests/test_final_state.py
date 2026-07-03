# test_final_state.py

import pytest
import requests
import time

def wait_for_server(url, timeout=5):
    """Wait for the server to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Just a simple GET to see if the port is open and responding, 
            # or we can just try to connect.
            requests.get(url)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    return False

def test_mcmc_endpoint():
    """Test the /run_mcmc endpoint to ensure it returns the correct posterior mean."""
    url = "http://127.0.0.1:9090/run_mcmc"

    # We don't strictly require wait_for_server to succeed on GET since the endpoint is POST,
    # but we can just wait by retrying the POST request.

    payload = {
        "iterations": 5000,
        "init_mu": 1.0
    }

    max_retries = 10
    response = None
    for _ in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=30)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)

    assert response is not None, f"Failed to connect to the server at {url}. Is the server running?"
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, but could not parse it. Response: {response.text}")

    assert "mean" in data, f"Response JSON does not contain 'mean' key. Response: {data}"

    mean_val = data["mean"]
    assert isinstance(mean_val, (int, float)), f"Expected 'mean' to be a number, got {type(mean_val)}"

    expected_mean = 1.234
    tolerance = 0.05

    assert abs(mean_val - expected_mean) <= tolerance, \
        f"Calculated mean {mean_val} is not within {tolerance} of expected {expected_mean}."