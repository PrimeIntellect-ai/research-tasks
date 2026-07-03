# test_final_state.py
import os
import json
import pytest
import requests
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import joblib
import importlib

def generate_expected_data():
    np.random.seed(42)
    X = np.random.randn(1000, 15)
    X[:, 6] = X[:, 2] * 0.95 + np.random.randn(1000) * 0.1
    X[:, 11] = X[:, 5] * 0.9 + np.random.randn(1000) * 0.1
    columns = [f'f{i+1}' for i in range(15)]
    df = pd.DataFrame(X, columns=columns)
    df['target'] = 2.5 * df['f1'] - 1.2 * df['f3'] + 0.8 * df['f8'] + np.random.randn(1000) * 0.5
    return df

def test_fast_tracker_installed():
    try:
        import fast_tracker
    except ImportError:
        pytest.fail("The 'fast-tracker' package is not installed or cannot be imported.")

def test_filtered_dataset():
    filtered_path = '/home/user/filtered_dataset.csv'
    assert os.path.isfile(filtered_path), f"Filtered dataset not found at {filtered_path}"

    df_filtered = pd.read_csv(filtered_path)
    expected_columns = [f'f{i+1}' for i in range(15) if i+1 not in (7, 12)] + ['target']

    assert list(df_filtered.columns) == expected_columns, f"Expected columns {expected_columns}, but got {list(df_filtered.columns)}"
    assert len(df_filtered) == 1000, f"Expected 1000 rows, but got {len(df_filtered)}"

def test_model_saved():
    model_path = '/home/user/model.pkl'
    assert os.path.isfile(model_path), f"Model not found at {model_path}"
    try:
        model = joblib.load(model_path)
        assert isinstance(model, Ridge), "Saved model is not a Ridge regression model."
    except Exception as e:
        pytest.fail(f"Failed to load model from {model_path}: {e}")

def test_service_endpoints():
    # Recompute expected model and MSE
    df = generate_expected_data()
    features = [c for c in df.columns if c not in ('f7', 'f12', 'target')]
    X = df[features]
    y = df['target']

    model = Ridge(random_state=42)
    model.fit(X, y)
    preds = model.predict(X)
    expected_mse = mean_squared_error(y, preds)

    # Test GET /metrics
    try:
        resp = requests.get("http://127.0.0.1:8080/metrics", timeout=5)
        assert resp.status_code == 200, f"GET /metrics returned status {resp.status_code}"
        data = resp.json()
        assert "mse" in data, "Response JSON missing 'mse' key"
        assert np.isclose(data["mse"], expected_mse, rtol=1e-3), f"Expected MSE ~{expected_mse}, got {data['mse']}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to GET /metrics: {e}")

    # Test POST /predict
    test_features = [0.1] * 13
    expected_pred = model.predict([test_features])[0]
    try:
        resp = requests.post("http://127.0.0.1:8080/predict", json={"features": test_features}, timeout=5)
        assert resp.status_code == 200, f"POST /predict returned status {resp.status_code}"
        data = resp.json()
        assert "prediction" in data, "Response JSON missing 'prediction' key"
        assert np.isclose(data["prediction"], expected_pred, rtol=1e-3), f"Expected prediction ~{expected_pred}, got {data['prediction']}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to POST /predict: {e}")