# test_final_state.py
import os
import requests
import pytest

def test_plot_exists():
    plot_path = '/home/user/pca_clusters.png'
    assert os.path.exists(plot_path), f"Plot file {plot_path} does not exist."
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty."

def test_ping_endpoint():
    try:
        response = requests.get('http://127.0.0.1:8080/ping', timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at 127.0.0.1:8080/ping: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /ping is not valid JSON.")

    assert data.get('message') == 'pong', f"Expected message 'pong', got {data.get('message')}"

def test_predict_endpoint():
    payload = {
        "pca_1": 0.0,
        "pca_2": 0.0,
        "age": 50.0,
        "heart_rate": 80.0
    }
    try:
        response = requests.post('http://127.0.0.1:8080/predict', json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at 127.0.0.1:8080/predict: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /predict is not valid JSON.")

    assert 'prediction' in data, f"Response JSON missing 'prediction' key. Got: {data}"
    assert data['prediction'] in [0, 1], f"Expected prediction to be 0 or 1, got {data['prediction']}"