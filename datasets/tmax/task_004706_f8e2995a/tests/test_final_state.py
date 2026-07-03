# test_final_state.py

import os
import requests
import pytest

def test_libtoken_built():
    """Ensure the shared object library was built successfully."""
    assert os.path.exists("/home/user/app/libtoken.so"), "libtoken.so was not built. Did you fix the Makefile and run make?"

def test_api_verify_no_crash():
    """
    Test the API endpoint with a long token to ensure the buffer overflow
    in the C library has been fixed and does not crash the Python process.
    """
    url = "http://127.0.0.1:8080/verify"
    payload = {"token": "A_VERY_LONG_USERNAME_THAT_EXCEEDS_SIXTEEN_BYTES_AND_THEN_SOME"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("API service on port 8080 is not reachable or crashed. The buffer overflow might not be fixed, or the service wasn't started.")
    except requests.exceptions.Timeout:
        pytest.fail("API service on port 8080 timed out.")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "result" in data, "Response JSON missing 'result' key."
    assert data["result"] in ["verified", "failed"], f"Unexpected result value: {data['result']}"

def test_metrics_service_reachable():
    """Ensure the metrics service is running and reachable."""
    url = "http://127.0.0.1:8081/stats"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Metrics service on port 8081 is not reachable. Did you start the services?")
    except requests.exceptions.Timeout:
        pytest.fail("Metrics service on port 8081 timed out.")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}."

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "reqs" in data, "Response JSON missing 'reqs' key."