# test_final_state.py
import requests
import time
import pytest

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer MATH-TOKEN-2024"}

def test_missing_auth():
    """Test that missing auth header returns 401."""
    response = requests.post(
        f"{BASE_URL}/evaluate",
        json={"expression": "R + G", "frame": 10}
    )
    assert response.status_code == 401, f"Expected 401 for missing auth, got {response.status_code}"

def test_invalid_auth():
    """Test that invalid auth header returns 401."""
    response = requests.post(
        f"{BASE_URL}/evaluate",
        headers={"Authorization": "Bearer INVALID-TOKEN"},
        json={"expression": "R + G", "frame": 10}
    )
    assert response.status_code == 401, f"Expected 401 for invalid auth, got {response.status_code}"

def test_invalid_frame():
    """Test that out-of-bounds frame returns 400."""
    response = requests.post(
        f"{BASE_URL}/evaluate",
        headers=AUTH_HEADER,
        json={"expression": "R + G", "frame": 150}
    )
    assert response.status_code == 400, f"Expected 400 for invalid frame, got {response.status_code}"

def test_valid_evaluation():
    """Test a valid mathematical evaluation using extracted RGB values."""
    # Frame 10: R = 50, G = 100, B = 150
    # Expression: R + G * B = 50 + 100 * 150 = 15050
    response = requests.post(
        f"{BASE_URL}/evaluate",
        headers=AUTH_HEADER,
        json={"expression": "R + G * B", "frame": 10}
    )
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code} with body {response.text}"

    data = response.json()
    assert "result" in data, "Response JSON missing 'result' key"
    assert data["result"] == 15050, f"Expected result 15050, got {data['result']}"

def test_rate_limiting():
    """Test that the API enforces a rate limit of 5 requests per second per IP."""
    # Use a unique mock IP to avoid interference with other tests
    headers = AUTH_HEADER.copy()
    headers["X-Forwarded-For"] = "192.168.1.100"

    status_codes = []
    # Send 10 requests rapidly
    for _ in range(10):
        response = requests.post(
            f"{BASE_URL}/evaluate",
            headers=headers,
            json={"expression": "R + G", "frame": 10}
        )
        status_codes.append(response.status_code)

    # We expect exactly 5 successes (200) and 5 rate limits (429)
    success_count = status_codes.count(200)
    rate_limit_count = status_codes.count(429)

    assert success_count == 5, f"Expected exactly 5 successful requests, got {success_count}. Status codes: {status_codes}"
    assert rate_limit_count == 5, f"Expected exactly 5 rate-limited requests (429), got {rate_limit_count}. Status codes: {status_codes}"