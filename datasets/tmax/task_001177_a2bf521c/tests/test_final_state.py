# test_final_state.py

import base64
import urllib.parse
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080/process"
API_KEY = "X7f9A2mP"

def test_missing_auth():
    """Test that requests without an Authorization header are rejected."""
    try:
        response = requests.post(BASE_URL, data={"text": "test"}, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth, got {response.status_code}"

def test_invalid_auth():
    """Test that requests with an invalid Authorization header are rejected."""
    headers = {"Authorization": "Bearer INVALID_KEY"}
    try:
        response = requests.post(BASE_URL, data={"text": "test"}, headers=headers, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid auth, got {response.status_code}"

def test_valid_request_simple():
    """Test a simple valid request to ensure decoding and encoding work."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = "text=Hello%20World%21"

    try:
        # We send raw data to ensure the exact payload is sent
        response = requests.post(BASE_URL, data=payload, headers=headers, 
                                 headers_update={"Content-Type": "application/x-www-form-urlencoded"}, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    expected_output = "SGVsbG8gV29ybGQh"
    actual_output = response.text.strip()
    assert actual_output == expected_output, f"Expected '{expected_output}', got '{actual_output}'"

def test_valid_request_long_payload():
    """Test a long payload to verify memory safety fixes."""
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Create a long string with URL encoding
    raw_text = "A" * 1000 + " " + "B" * 1000 + "!"
    url_encoded_text = urllib.parse.quote(raw_text)
    payload = f"text={url_encoded_text}"

    try:
        response = requests.post(BASE_URL, data=payload, headers=headers,
                                 headers_update={"Content-Type": "application/x-www-form-urlencoded"}, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server or server crashed: {e}")

    assert response.status_code == 200, f"Expected 200 OK for long payload, got {response.status_code}"

    expected_output = base64.b64encode(raw_text.encode('utf-8')).decode('utf-8')
    actual_output = response.text.strip()
    assert actual_output == expected_output, "Base64 output for long payload did not match expected value."