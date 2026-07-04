# test_final_state.py

import pytest
import requests
import time

def test_middleware_analyze_endpoint():
    """Test that the middleware service returns correct analytical results on /analyze."""
    url = "http://127.0.0.1:8080/analyze"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the middleware service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK on /analyze, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    assert "dominant_freq" in data, f"Missing 'dominant_freq' in JSON response: {data}"
    assert "ci_lower" in data, f"Missing 'ci_lower' in JSON response: {data}"
    assert "ci_upper" in data, f"Missing 'ci_upper' in JSON response: {data}"

    try:
        freq = float(data["dominant_freq"])
        ci_lower = float(data["ci_lower"])
        ci_upper = float(data["ci_upper"])
    except ValueError:
        pytest.fail(f"JSON response values must be convertible to floats. Got: {data}")

    assert abs(freq - 15.0) < 0.5, f"Dominant frequency {freq} is not close to expected 15.0 Hz"
    assert 4.5 < ci_lower < 5.0, f"ci_lower {ci_lower} is out of expected bounds (4.5, 5.0)"
    assert 5.0 < ci_upper < 5.5, f"ci_upper {ci_upper} is out of expected bounds (5.0, 5.5)"

def test_middleware_404_endpoint():
    """Test that the middleware service returns 404 for unknown routes."""
    url = "http://127.0.0.1:8080/unknown"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the middleware service at {url}: {e}")

    assert response.status_code == 404, f"Expected HTTP 404 Not Found on /unknown, got {response.status_code}. Response body: {response.text}"