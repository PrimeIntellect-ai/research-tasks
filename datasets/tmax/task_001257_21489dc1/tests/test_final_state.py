# test_final_state.py
import os
import json
import pytest
import requests

def test_makefile_exists():
    assert os.path.isfile("/app/Makefile"), "Makefile does not exist in /app/"

def test_go_test_file_exists():
    assert os.path.isfile("/app/src/go-server/poly_test.go"), "poly_test.go does not exist in /app/src/go-server/"

def test_http_server_unauthorized():
    url = "http://127.0.0.1:8080/poly/eval"
    payload = {"coeffs": [2.0, -1.0, 3.0], "x": 4.0}

    # Missing auth header
    try:
        response = requests.post(url, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth header, got {response.status_code}"

    # Invalid auth header
    headers = {"Authorization": "Bearer INVALID_TOKEN"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid auth header, got {response.status_code}"

def test_http_server_authorized_eval():
    url = "http://127.0.0.1:8080/poly/eval"
    payload = {"coeffs": [2.0, -1.0, 3.0], "x": 4.0}
    headers = {"Authorization": "Bearer SIGMA_7781"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "result" in data, "Response JSON missing 'result' key"
    assert abs(data["result"] - 46.0) < 1e-6, f"Expected result 46.0, got {data['result']}"

def test_http_server_large_poly():
    url = "http://127.0.0.1:8080/poly/eval"
    # Create a large polynomial to test memory leaks/crashes
    degree = 10000
    coeffs = [1.0] * (degree + 1)
    payload = {"coeffs": coeffs, "x": 1.0}
    headers = {"Authorization": "Bearer SIGMA_7781"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to evaluate large polynomial (server might have crashed): {e}")

    assert response.status_code == 200, f"Expected 200 OK for large polynomial, got {response.status_code}"
    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "result" in data, "Response JSON missing 'result' key"
    assert abs(data["result"] - (degree + 1)) < 1e-6, f"Expected result {degree + 1}, got {data['result']}"