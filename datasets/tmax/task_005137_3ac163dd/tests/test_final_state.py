# test_final_state.py

import os
import json
import pickle
import pytest
import requests
import numpy as np
import sys

def test_datacleaner_fixed():
    # Add vendored path to sys.path to import it
    vendored_path = "/app/vendored/datacleaner-1.0.0"
    if vendored_path not in sys.path:
        sys.path.insert(0, vendored_path)

    try:
        from datacleaner.core import prepare_and_split
    except ImportError:
        pytest.fail("Could not import prepare_and_split from datacleaner.core")

    # Create a synthetic dataset with an extreme outlier in the test set
    # 100 rows, 2 features. test_size=0.2 means last 20 rows are test set (if not shuffled, but train_test_split shuffles by default unless shuffle=False. Wait, train_test_split shuffles by default with random_state=42. We need to ensure the outlier goes to the test set, or we can just check if scaler was fit on 80 samples instead of 100).
    # Actually, we can just check if scaler.n_samples_seen_ == 80 when total is 100 and test_size=0.2.
    X = np.random.rand(100, 2)
    y = np.random.randint(0, 2, 100)

    try:
        result = prepare_and_split(X, y, test_size=0.2, random_state=42)
    except Exception as e:
        pytest.fail(f"prepare_and_split raised an exception: {e}")

    assert len(result) == 5, "prepare_and_split should return 5 items: X_train, X_test, y_train, y_test, scaler"
    X_train, X_test, y_train, y_test, scaler = result

    assert hasattr(scaler, "n_samples_seen_"), "Returned scaler does not appear to be a fitted StandardScaler"
    assert scaler.n_samples_seen_ == 80, f"Scaler should be fitted on 80 samples, but saw {scaler.n_samples_seen_}. This indicates data leakage."

def test_model_and_scaler_exist():
    model_path = "/home/user/model.pkl"
    scaler_path = "/home/user/scaler.pkl"

    assert os.path.exists(model_path), f"{model_path} does not exist"
    assert os.path.exists(scaler_path), f"{scaler_path} does not exist"

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    assert type(model).__name__ == "RandomForestClassifier", "Model is not a RandomForestClassifier"

    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    assert type(scaler).__name__ == "StandardScaler", "Scaler is not a StandardScaler"

def test_metrics_json_exists_and_valid():
    metrics_path = "/home/user/metrics.json"
    assert os.path.exists(metrics_path), f"{metrics_path} does not exist"

    with open(metrics_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{metrics_path} is not valid JSON")

    assert "inference_time_seconds" in metrics, "Key 'inference_time_seconds' missing in metrics.json"
    assert isinstance(metrics["inference_time_seconds"], (int, float)), "inference_time_seconds must be a number"

def test_web_service_auth_missing():
    url = "http://127.0.0.1:8080/predict"
    payload = {"features": [1000, 20, 0.05, 1.2]}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to web service: {e}")

    assert response.status_code == 401, f"Expected 401 for missing auth, got {response.status_code}"

def test_web_service_auth_incorrect():
    url = "http://127.0.0.1:8080/predict"
    payload = {"features": [1000, 20, 0.05, 1.2]}
    headers = {"Authorization": "Bearer WRONG-TOKEN"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to web service: {e}")

    assert response.status_code == 401, f"Expected 401 for incorrect auth, got {response.status_code}"

def test_web_service_success():
    url = "http://127.0.0.1:8080/predict"
    payload = {"features": [1000, 20, 0.05, 1.2]}
    headers = {"Authorization": "Bearer RESEARCH-SEC-2024"}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to web service: {e}")

    assert response.status_code == 200, f"Expected 200 for valid request, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "prediction" in data, f"Key 'prediction' missing in response: {data}"
    assert isinstance(data["prediction"], int), f"Prediction should be an integer, got {type(data['prediction'])}"