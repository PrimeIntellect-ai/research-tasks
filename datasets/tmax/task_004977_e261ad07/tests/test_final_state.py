# test_final_state.py
import os
import requests
import pytest

def test_libcode_so_exists():
    """Verify that the compiled shared library exists."""
    lib_path = "/home/user/libcode.so"
    assert os.path.exists(lib_path), f"Missing required shared library: {lib_path}"
    assert os.path.isfile(lib_path), f"Expected {lib_path} to be a file."

def test_api_code():
    """Verify the /api/code endpoint returns the correct decoded DTMF sequence."""
    url = "http://127.0.0.1:8888/api/code"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response: {response.text}")

    assert "code" in data, f"JSON response missing 'code' key. Response: {data}"
    assert data["code"] == 8675309, f"Expected code to be 8675309, got {data['code']}"

def test_api_data():
    """Verify the /api/data endpoint returns the correctly processed and sorted data."""
    url = "http://127.0.0.1:8888/api/data"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Response: {response.text}")

    assert "data" in data, f"JSON response missing 'data' key. Response: {data}"

    expected_data = ["apple", "banana", "cherry", "date", "elderberry"]
    assert data["data"] == expected_data, f"Expected data list {expected_data}, got {data['data']}"