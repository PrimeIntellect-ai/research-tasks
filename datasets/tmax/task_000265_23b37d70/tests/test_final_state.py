# test_final_state.py

import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer perf-token-2024"}

def test_unauthorized_request():
    """Test that a request without the proper authorization header is rejected."""
    try:
        response = requests.get(f"{BASE_URL}/predict?x=10", timeout=2)
        # We expect a non-200 response
        assert response.status_code != 200, f"Expected non-200 status code for unauthorized request, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        # Connection drop is also acceptable as per truth
        pass

def test_authorized_request_x25():
    """Test authorized request for x=25, expecting Y=1180."""
    try:
        response = requests.get(f"{BASE_URL}/predict?x=25", headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the service at 127.0.0.1:8080")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    body = response.text.strip()
    assert body == "1180", f"Expected prediction '1180' for x=25, got '{body}'"

def test_authorized_request_x30():
    """Test authorized request for x=30, expecting Y=1715."""
    try:
        response = requests.get(f"{BASE_URL}/predict?x=30", headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the service at 127.0.0.1:8080")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    body = response.text.strip()
    assert body == "1715", f"Expected prediction '1715' for x=30, got '{body}'"