# test_final_state.py

import os
import requests
import pytest

def test_shared_library_compiled():
    """Verify that the shared library was compiled."""
    so_path = "/home/user/project/libchecksum.so"
    assert os.path.isfile(so_path), f"Shared library missing at {so_path}. Did the Makefile run successfully?"

def test_http_server_compute_compatible():
    """Test the /compute endpoint with a compatible version."""
    url = "http://127.0.0.1:8080/compute"
    headers = {"X-Client-Version": "2.5.0"}
    data = b"hello" # sum = 104 + 101 + 108 + 108 + 111 = 532

    try:
        response = requests.post(url, headers=headers, data=data, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        json_resp = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "checksum" in json_resp, "Response JSON missing 'checksum' key"
    assert "compatible" in json_resp, "Response JSON missing 'compatible' key"

    assert json_resp["checksum"] == 1115, f"Expected checksum 1115, got {json_resp['checksum']}"
    assert json_resp["compatible"] is True, f"Expected compatible to be True, got {json_resp['compatible']}"

def test_http_server_compute_incompatible_major():
    """Test the /compute endpoint with an incompatible major version."""
    url = "http://127.0.0.1:8080/compute"
    headers = {"X-Client-Version": "3.0.0"}
    data = b"test" # sum = 116 + 101 + 115 + 116 = 448

    try:
        response = requests.post(url, headers=headers, data=data, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        json_resp = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert json_resp["checksum"] == 1031, f"Expected checksum 1031, got {json_resp['checksum']}"
    assert json_resp["compatible"] is False, f"Expected compatible to be False, got {json_resp['compatible']}"

def test_http_server_compute_incompatible_minor():
    """Test the /compute endpoint with an incompatible minor version."""
    url = "http://127.0.0.1:8080/compute"
    headers = {"X-Client-Version": "2.0.9"}
    data = b"foo" # sum = 102 + 111 + 111 = 324

    try:
        response = requests.post(url, headers=headers, data=data, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        json_resp = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert json_resp["checksum"] == 907, f"Expected checksum 907, got {json_resp['checksum']}"
    assert json_resp["compatible"] is False, f"Expected compatible to be False, got {json_resp['compatible']}"

def test_http_server_compute_exact_version():
    """Test the /compute endpoint with the exact API version."""
    url = "http://127.0.0.1:8080/compute"
    headers = {"X-Client-Version": "2.1.0"}
    data = b"A" # sum = 65

    try:
        response = requests.post(url, headers=headers, data=data, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        json_resp = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert json_resp["checksum"] == 648, f"Expected checksum 648, got {json_resp['checksum']}"
    assert json_resp["compatible"] is True, f"Expected compatible to be True, got {json_resp['compatible']}"