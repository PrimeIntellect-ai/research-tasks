# test_final_state.py
import pytest
import requests
import time
import socket

API_URL = "http://127.0.0.1:9090/api/v1/stats"
TOKEN = "ZETA_99_OMEGA"

def wait_for_port(host, port, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (ConnectionRefusedError, TimeoutError, OSError):
            time.sleep(0.5)
    return False

def test_server_listening():
    """Verify that the API server is listening on port 9090."""
    assert wait_for_port("127.0.0.1", 9090), "Server is not listening on 127.0.0.1:9090"

def test_auth_missing():
    """Verify that the endpoint returns 401 when the Authorization header is missing."""
    response = requests.get(f"{API_URL}?var1=Temp&var2=Pressure")
    assert response.status_code == 401, f"Expected 401 Unauthorized when missing token, got {response.status_code}"

def test_auth_invalid():
    """Verify that the endpoint returns 401 when the Authorization header is invalid."""
    headers = {"Authorization": "Bearer INVALID_TOKEN"}
    response = requests.get(f"{API_URL}?var1=Temp&var2=Pressure", headers=headers)
    assert response.status_code == 401, f"Expected 401 Unauthorized when token is invalid, got {response.status_code}"

def test_valid_request_and_math():
    """Verify that a valid request returns 200, correct JSON keys, and accurate math metrics."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{API_URL}?var1=Temp&var2=Pressure", headers=headers)

    assert response.status_code == 200, f"Expected 200 OK for valid request, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    expected_keys = {"covariance", "correlation", "ci_lower", "ci_upper"}
    assert set(data.keys()) == expected_keys, f"JSON keys do not match expected keys. Got: {list(data.keys())}"

    # Expected values
    expected_correlation = 0.6489
    expected_covariance = 46.6806
    expected_ci_lower = 0.4578
    expected_ci_upper = 0.7824

    tolerance = 0.005

    assert abs(data["correlation"] - expected_correlation) <= tolerance, f"Correlation {data['correlation']} is not within {tolerance} of {expected_correlation}"
    assert abs(data["covariance"] - expected_covariance) <= tolerance, f"Covariance {data['covariance']} is not within {tolerance} of {expected_covariance}"
    assert abs(data["ci_lower"] - expected_ci_lower) <= tolerance, f"ci_lower {data['ci_lower']} is not within {tolerance} of {expected_ci_lower}"
    assert abs(data["ci_upper"] - expected_ci_upper) <= tolerance, f"ci_upper {data['ci_upper']} is not within {tolerance} of {expected_ci_upper}"