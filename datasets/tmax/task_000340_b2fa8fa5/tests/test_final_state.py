# test_final_state.py

import pytest
import requests
import time

API_URL = "http://127.0.0.1:9090/api/scan"

def wait_for_service(url, timeout=5):
    """Wait for the Go service to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # A simple GET or OPTIONS might fail, but we just want to see if the port is open.
            # We'll just try connecting via requests.
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def test_service_is_running():
    """Test that the API wrapper service is listening and reachable."""
    # We don't strictly need it to return 200 for GET, just need it to accept connections.
    try:
        requests.options(API_URL, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("The Go web service is not running or not listening on 127.0.0.1:9090")

def test_scan_port_8080():
    """Test that scanning port 8080 returns decrypted and redacted JSON."""
    payload = {"target_ip": "10.0.0.5", "target_port": "8080"}
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    assert data.get("service") == "http", "Expected 'service' to be 'http'"
    assert data.get("status") == "vulnerable", "Expected 'status' to be 'vulnerable'"
    assert data.get("details") == "exposed admin panel", "Expected 'details' to be 'exposed admin panel'"

    # Check redaction
    assert "api_token" in data, "The 'api_token' key is missing from the response."
    assert data["api_token"] == "[REDACTED]", f"Expected 'api_token' to be '[REDACTED]', but got '{data['api_token']}'"

def test_scan_port_3306():
    """Test that scanning port 3306 returns decrypted and redacted JSON."""
    payload = {"target_ip": "10.0.0.5", "target_port": "3306"}
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    assert data.get("service") == "mysql", "Expected 'service' to be 'mysql'"
    assert data.get("vulnerability") == "empty root password", "Expected 'vulnerability' to be 'empty root password'"

    # Check redaction
    assert "password" in data, "The 'password' key is missing from the response."
    assert data["password"] == "[REDACTED]", f"Expected 'password' to be '[REDACTED]', but got '{data['password']}'"