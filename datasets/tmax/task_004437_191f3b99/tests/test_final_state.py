# test_final_state.py
import os
import pytest
import requests

def test_libdecoder_exists():
    """Verify that the compiled C shared library exists."""
    lib_path = "/home/user/libdecoder.so"
    assert os.path.isfile(lib_path), f"The C shared library {lib_path} does not exist."

def test_api_unauthorized():
    """Verify that the API returns 401 when the authorization header is missing or incorrect."""
    url = "http://127.0.0.1:8080/api/v1/extract"
    payload = {"image_path": "/app/data/config_scan.png"}

    # Missing header
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth header, got {response.status_code}. Response: {response.text}"

    # Incorrect header
    headers = {"Authorization": "Bearer invalid-token-123"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for incorrect auth header, got {response.status_code}. Response: {response.text}"

def test_api_not_found():
    """Verify that the API returns 404 when the requested image does not exist."""
    url = "http://127.0.0.1:8080/api/v1/extract"
    payload = {"image_path": "/app/data/nonexistent.png"}
    headers = {"Authorization": "Bearer dev-secret-token-99"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 404, f"Expected 404 Not Found for non-existent image, got {response.status_code}. Response: {response.text}"

def test_api_success():
    """Verify that the API returns 200 and the correctly decoded value for a valid request."""
    url = "http://127.0.0.1:8080/api/v1/extract"
    payload = {"image_path": "/app/data/config_scan.png"}
    headers = {"Authorization": "Bearer dev-secret-token-99"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Failed to parse JSON response. Response text: {response.text}")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"

    # The text in the image is "5 12 7 2"
    # Polynomial evaluation at x=3:
    # 5*(3^0) + 12*(3^1) + 7*(3^2) + 2*(3^3)
    # = 5*1 + 12*3 + 7*9 + 2*27
    # = 5 + 36 + 63 + 54 = 158
    # XOR with 42:
    # 158 ^ 42 = 180
    expected_val = 180
    assert data.get("decoded_value") == expected_val, f"Expected decoded_value {expected_val}, got {data.get('decoded_value')}"