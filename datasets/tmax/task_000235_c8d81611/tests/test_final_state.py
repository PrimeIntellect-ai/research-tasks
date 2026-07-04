# test_final_state.py

import pytest
import requests

SERVICE_URL = "http://127.0.0.1:8080/transform"

def test_service_is_running():
    """Verify that the service is running and accessible."""
    try:
        response = requests.post(SERVICE_URL, data="ping:pong", timeout=5)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running on 127.0.0.1:8080 or refused the connection.")
    except requests.exceptions.Timeout:
        pytest.fail("Service at 127.0.0.1:8080 timed out.")

def test_transform_normal_input():
    """Verify that normal key-value pairs are correctly transformed to JSON."""
    payload = "key1:value1|key2:value2"
    try:
        response = requests.post(SERVICE_URL, data=payload, timeout=5)
    except Exception as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected = {"key1": "value1", "key2": "value2"}
    assert data == expected, f"Expected {expected}, got {data}"

def test_transform_drops_empty_values():
    """Verify that keys with empty values are dropped from the resulting JSON."""
    payload = "key1:value1|key2:|key3:value3|key4:"
    try:
        response = requests.post(SERVICE_URL, data=payload, timeout=5)
    except Exception as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected = {"key1": "value1", "key3": "value3"}
    assert data == expected, f"Expected {expected}, got {data}. Empty values must be dropped."

def test_transform_multiple_colons():
    """Verify that values containing colons are handled correctly (split only by the first colon)."""
    payload = "url:http://example.com|time:12:34:56"
    try:
        response = requests.post(SERVICE_URL, data=payload, timeout=5)
    except Exception as e:
        pytest.fail(f"Request failed: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected = {"url": "http://example.com", "time": "12:34:56"}
    assert data == expected, f"Expected {expected}, got {data}"