# test_final_state.py

import pytest
import requests
import time

GATEWAY_URL = "http://127.0.0.1:8080/analyze"

def wait_for_service(url, timeout=5):
    """Wait for the gateway service to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Just a simple GET or POST to check if the port is open
            requests.post(url, data="test", timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    return False

def test_gateway_normal_sequence():
    """Test that the gateway handles a normal sequence correctly."""
    assert wait_for_service(GATEWAY_URL), "Gateway service is not running or not listening on port 8080."

    seq = "ATGC"
    try:
        response = requests.post(GATEWAY_URL, data=seq, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to gateway: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "alignment" in data, "Response JSON missing 'alignment' key."
    assert "spectrum" in data, "Response JSON missing 'spectrum' key."
    assert data["alignment"] == {"score": 8}, f"Expected alignment score 8, got {data['alignment']}"
    assert data["spectrum"] == {"dominant_freq": 0.33}, f"Expected spectrum dominant_freq 0.33, got {data['spectrum']}"

def test_gateway_singular_sequence():
    """Test that the gateway handles a singular sequence (fallback) correctly."""
    assert wait_for_service(GATEWAY_URL), "Gateway service is not running or not listening on port 8080."

    seq = "AAAA"
    try:
        response = requests.post(GATEWAY_URL, data=seq, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to gateway: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "alignment" in data, "Response JSON missing 'alignment' key."
    assert "error" in data, "Response JSON missing 'error' key."
    assert data["error"] == "near-singular sequence detected", f"Unexpected error message: {data['error']}"
    assert data["alignment"] == {"score": 8}, f"Expected alignment score 8, got {data['alignment']}"
    assert "spectrum" not in data, "Response JSON should not contain 'spectrum' on fallback."