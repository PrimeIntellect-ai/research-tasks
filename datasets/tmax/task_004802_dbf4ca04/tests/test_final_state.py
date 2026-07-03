# test_final_state.py
import os
import json
import pytest
import requests

def test_experiment_results_exists_and_valid():
    results_path = "/home/user/experiment_results.json"
    assert os.path.exists(results_path), f"Results file {results_path} is missing. Did you save the experiment results?"

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Experiment results file {results_path} is not valid JSON.")

    assert "train_mse" in data, "Key 'train_mse' is missing from experiment results JSON."
    assert isinstance(data["train_mse"], float), "Value for 'train_mse' must be a float."

def test_api_unauthorized_access():
    url = "http://127.0.0.1:8080/predict"
    payload = {"text": "Data SCIENCE is fun."}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}. Is the server running? Error: {e}")

    assert response.status_code in (401, 403), (
        f"Expected 401 or 403 for request without API key, got {response.status_code}. "
        f"Response body: {response.text}"
    )

def test_api_authorized_access_and_prediction():
    url = "http://127.0.0.1:8080/predict"
    payload = {"text": "Data SCIENCE is fun."}
    headers = {"X-API-Key": "DS-CLEAN-2024"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}. Is the server running? Error: {e}")

    assert response.status_code == 200, (
        f"Expected 200 OK for authorized request, got {response.status_code}. "
        f"Response body: {response.text}"
    )

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"API response is not valid JSON. Response body: {response.text}")

    assert "cleaned_text" in data, "Key 'cleaned_text' missing from API response."
    assert "prediction" in data, "Key 'prediction' missing from API response."

    expected_cleaned = "data science is fun"
    assert data["cleaned_text"] == expected_cleaned, (
        f"Expected cleaned text '{expected_cleaned}', got '{data['cleaned_text']}'"
    )
    assert isinstance(data["prediction"], float), "Prediction must be a float."