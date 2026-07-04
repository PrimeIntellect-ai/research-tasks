# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer RES-8821"}

def test_health_no_auth():
    """Test that /health returns 401 Unauthorized without auth header."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}. Response: {response.text}"

def test_health_with_auth():
    """Test that /health returns 200 and {'status': 'ok'} with auth header."""
    try:
        response = requests.get(f"{BASE_URL}/health", headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"

def test_optimal_k():
    """Test that /optimal_k returns 200 and the correct optimal k."""
    try:
        response = requests.get(f"{BASE_URL}/optimal_k", headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "k" in data, f"Expected key 'k' in response, got {data}"
    assert data["k"] == 2, f"Expected optimal k to be 2, got {data['k']}"

def test_predict():
    """Test that /predict returns 200 and the correct prediction."""
    try:
        response = requests.get(f"{BASE_URL}/predict", headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "prediction" in data, f"Expected key 'prediction' in response, got {data}"

    prediction = float(data["prediction"])
    assert abs(prediction - 127.0) < 1e-5, f"Expected prediction to be 127.0, got {prediction}"