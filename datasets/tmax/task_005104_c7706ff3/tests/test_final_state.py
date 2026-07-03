# test_final_state.py

import os
import json
import time
import pytest
import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import BayesianRidge

def get_expected_model_and_features():
    df = pd.read_csv('/home/user/data/server_metrics.csv')

    # Impute missing cpu_usage with median
    median_cpu = df['cpu_usage'].median()
    df['cpu_usage'] = df['cpu_usage'].fillna(median_cpu)

    # Remove disk_io > 1000
    df = df[df['disk_io'] <= 1000].copy()

    # Compute correlations
    corr = df.corr().abs()
    latency_corr = corr['latency'].drop('latency')
    top_2_features = latency_corr.nlargest(2).index.tolist()

    # Train Bayesian Ridge
    X = df[top_2_features]
    y = df['latency']
    model = BayesianRidge()
    model.fit(X, y)

    return model, top_2_features

def test_experiment_json():
    json_path = "/home/user/experiment.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "alpha" in data, "Key 'alpha' missing from experiment.json."
    assert "lambda" in data, "Key 'lambda' missing from experiment.json."

def test_health_endpoint():
    url = "http://127.0.0.1:8080/health"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /health is not valid JSON.")

    assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"

def test_predict_endpoint():
    model, top_2_features = get_expected_model_and_features()

    url = "http://127.0.0.1:8080/predict"

    # Test payload
    payload = {top_2_features[0]: 50.0, top_2_features[1]: 50.0}

    # Expected prediction
    expected_pred = model.predict(pd.DataFrame([payload]))[0]

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /predict is not valid JSON.")

    assert "predicted_latency" in data, "Key 'predicted_latency' missing from response."

    predicted_latency = data["predicted_latency"]
    assert isinstance(predicted_latency, (int, float)), "predicted_latency must be a number."

    # Allow a small tolerance for floating point differences
    assert abs(predicted_latency - expected_pred) < 1.0, f"Expected prediction around {expected_pred}, got {predicted_latency}"