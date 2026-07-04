# test_final_state.py

import requests
import pytest

def test_server_running_and_processing_overflow_case():
    """
    Test that the server is running on 127.0.0.1:8080 and correctly handles
    the values extracted from the image without overflowing.
    """
    url = "http://127.0.0.1:8080/process?sn=2147483&key=1500"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    body = response.text.strip()
    expected_hash = "3221224500"
    assert body == expected_hash, f"Expected body to be '{expected_hash}', but got '{body}'. Integer overflow might not be fixed."

def test_server_running_and_processing_normal_case():
    """
    Test that the server correctly handles normal values.
    """
    url = "http://127.0.0.1:8080/process?sn=1000&key=1000"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    body = response.text.strip()
    expected_hash = "1000000"
    assert body == expected_hash, f"Expected body to be '{expected_hash}', but got '{body}'."