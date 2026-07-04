# test_final_state.py

import pytest
import requests
import time

API_URL = "http://127.0.0.1:8080/analyze"

def wait_for_server(url, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            # Just test connection, don't care about response for this check
            requests.get("http://127.0.0.1:8080/")
            return True
        except requests.ConnectionError:
            time.sleep(0.5)
    return False

@pytest.fixture(scope="module", autouse=True)
def ensure_server_running():
    assert wait_for_server(API_URL, timeout=10), "Server is not running or not accepting connections on 127.0.0.1:8080"

def test_full_range():
    payload = {"start_frame": 0, "end_frame": 299}
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {API_URL} failed: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "dominant_frequency_hz" in data, "Missing 'dominant_frequency_hz' in response"
    assert "is_significant" in data, "Missing 'is_significant' in response"

    assert abs(data["dominant_frequency_hz"] - 4.5) <= 0.2, f"Expected dominant frequency around 4.5 Hz, got {data['dominant_frequency_hz']}"
    assert data["is_significant"] is True, "Expected 'is_significant' to be true for the full range"

def test_short_noise_range():
    payload = {"start_frame": 10, "end_frame": 12}
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {API_URL} failed: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "dominant_frequency_hz" in data, "Missing 'dominant_frequency_hz' in response"
    assert "is_significant" in data, "Missing 'is_significant' in response"

    assert data["is_significant"] is False, "Expected 'is_significant' to be false for a very short range"

def test_partial_range():
    payload = {"start_frame": 30, "end_frame": 89}
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Request to {API_URL} failed: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "dominant_frequency_hz" in data, "Missing 'dominant_frequency_hz' in response"
    assert "is_significant" in data, "Missing 'is_significant' in response"

    assert abs(data["dominant_frequency_hz"] - 4.5) <= 0.2, f"Expected dominant frequency around 4.5 Hz, got {data['dominant_frequency_hz']}"
    assert data["is_significant"] is True, "Expected 'is_significant' to be true for the partial range"