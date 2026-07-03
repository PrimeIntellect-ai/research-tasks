# test_final_state.py
import os
import json
import pytest
import requests
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score

def test_features_csv_exists_and_valid():
    features_path = '/home/user/features.csv'
    assert os.path.isfile(features_path), f"{features_path} is missing."
    df = pd.read_csv(features_path)
    expected_columns = {'frame_index', 'mean_brightness', 'std_brightness'}
    assert expected_columns.issubset(df.columns), f"Columns in {features_path} do not match expected. Found: {list(df.columns)}"
    assert len(df) > 0, f"{features_path} is empty."

def test_experiment_log_exists_and_valid():
    log_path = '/home/user/experiment_log.json'
    assert os.path.isfile(log_path), f"{log_path} is missing."
    with open(log_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{log_path} is not valid JSON.")
    assert "cv_nmse" in data, f"'cv_nmse' key missing in {log_path}."
    assert isinstance(data["cv_nmse"], (int, float)), "'cv_nmse' must be a number."

def test_prediction_endpoint():
    features_path = '/home/user/features.csv'
    targets_path = '/app/targets.csv'

    # Check if files exist before proceeding
    assert os.path.isfile(features_path), f"{features_path} is missing."
    assert os.path.isfile(targets_path), f"{targets_path} is missing."

    features_df = pd.read_csv(features_path)
    targets_df = pd.read_csv(targets_path)

    merged_df = pd.merge(features_df, targets_df, on='frame_index')
    assert len(merged_df) > 0, "Merged dataset is empty."

    X = merged_df[['mean_brightness', 'std_brightness']]
    y = merged_df['target_value']

    # Train the golden pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('ridge', Ridge(alpha=1.0))
    ])
    pipeline.fit(X, y)

    # Test payloads
    test_cases = [
        {"mean_brightness": 100.5, "std_brightness": 25.0},
        {"mean_brightness": 50.0, "std_brightness": 10.0},
        {"mean_brightness": 200.0, "std_brightness": 50.0}
    ]

    url = "http://127.0.0.1:8080/predict"

    for payload in test_cases:
        try:
            response = requests.post(url, json=payload, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to {url}: {e}")

        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

        try:
            resp_json = response.json()
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {response.text}")

        assert "prediction" in resp_json, f"'prediction' key missing in response: {resp_json}"

        pred_val = resp_json["prediction"]
        assert isinstance(pred_val, (int, float)), f"Prediction must be a number, got {type(pred_val)}"

        # Calculate expected prediction
        expected_pred = pipeline.predict(pd.DataFrame([payload]))[0]

        # Allow a small margin of error due to potential floating point differences
        assert abs(pred_val - expected_pred) < 1e-3, f"Expected prediction ~{expected_pred:.4f}, but got {pred_val} for payload {payload}"