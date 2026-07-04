# test_final_state.py

import pytest
import requests
import time

API_URL = "http://127.0.0.1:8080/predict"
AUTH_TOKEN = "secret-token-123"

def wait_for_server(url, timeout=5):
    """Wait for the server to be up and running."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Send a GET or simple POST request to see if the port is open
            requests.get("http://127.0.0.1:8080/")
            return True
        except requests.ConnectionError:
            time.sleep(0.5)
    return False

def test_api_predict_success():
    """Test the /predict endpoint with correct authentication and payload."""
    # Wait briefly for the server to be available
    wait_for_server(API_URL)

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "temp": 25.5,
        "pressure": 1.2,
        "red_intensity": 150.4
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {API_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "prediction" in data, f"Key 'prediction' not found in response JSON: {data}"
    assert isinstance(data["prediction"], (int, float)), f"Prediction value should be a number, got {type(data['prediction'])}"

def test_api_predict_unauthorized():
    """Test the /predict endpoint with missing or incorrect authentication."""
    wait_for_server(API_URL)

    headers = {
        "Authorization": "Bearer wrong-token",
        "Content-Type": "application/json"
    }
    payload = {
        "temp": 25.5,
        "pressure": 1.2,
        "red_intensity": 150.4
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {API_URL}: {e}")

    assert response.status_code in (401, 403), f"Expected status code 401 or 403 for unauthorized request, got {response.status_code}"

def test_api_predict_missing_auth():
    """Test the /predict endpoint with no authentication header."""
    wait_for_server(API_URL)

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "temp": 25.5,
        "pressure": 1.2,
        "red_intensity": 150.4
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {API_URL}: {e}")

    assert response.status_code in (401, 403), f"Expected status code 401 or 403 for request missing auth header, got {response.status_code}"