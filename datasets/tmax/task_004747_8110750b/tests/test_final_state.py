# test_final_state.py
import pytest
import requests
import time

def test_api_merge_endpoint():
    """Test the /api/merge endpoint for correct sorting and merging."""
    url = "http://127.0.0.1:8080/api/merge"
    params = {
        "seq": "5,12,1",
        "file": "test_sequence"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_result = [1, 5, 8, 12, 19, 42]
    assert "result" in data, "Response JSON missing 'result' key."
    assert data["result"] == expected_result, f"Expected result {expected_result}, got {data['result']}"

def test_api_merge_endpoint_different_seq():
    """Test the /api/merge endpoint with a different sequence to ensure mathematical sorting."""
    url = "http://127.0.0.1:8080/api/merge"
    params = {
        "seq": "100,2",
        "file": "test_sequence"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    expected_result = [2, 8, 19, 42, 100]
    assert data.get("result") == expected_result, f"Expected mathematically sorted result {expected_result}, got {data.get('result')}"

def test_rate_limiting():
    """Test that Nginx enforces a rate limit of 5 requests per second."""
    url = "http://127.0.0.1:8080/api/merge"
    params = {
        "seq": "1",
        "file": "test_sequence"
    }

    # Send 10 rapid requests
    status_codes = []
    for _ in range(10):
        try:
            resp = requests.get(url, params=params, timeout=2)
            status_codes.append(resp.status_code)
        except requests.exceptions.RequestException:
            # If the connection is dropped, we can count it as a failure or rate limit, 
            # but Nginx normally returns 503.
            pass

    # At least one request should be rate-limited (503)
    assert 503 in status_codes, f"Expected rate limiting (HTTP 503) for rapid requests. Got status codes: {status_codes}"
    # At least one request should succeed (200)
    assert 200 in status_codes, f"Expected at least one successful request. Got status codes: {status_codes}"