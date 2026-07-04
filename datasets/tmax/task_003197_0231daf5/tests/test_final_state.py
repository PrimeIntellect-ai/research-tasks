# test_final_state.py

import os
import csv
import requests
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pytest

RAW_DATA_PATH = "/app/data/raw_features.csv"
PROCESSED_DATA_PATH = "/home/user/processed_features.csv"
MODEL_PATH = "/home/user/pca_model.pkl"
LOG_PATH = "/home/user/server.log"
BASE_URL = "http://127.0.0.1:8080"
TOKEN = "secret_ml_token_99X"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_files_exist():
    assert os.path.isfile("/home/user/etl_pipeline.py"), "ETL script missing at /home/user/etl_pipeline.py"
    assert os.path.isfile("/home/user/serve_features.py"), "Serve script missing at /home/user/serve_features.py"
    assert os.path.isfile(MODEL_PATH), f"PCA model missing at {MODEL_PATH}"
    assert os.path.isfile(PROCESSED_DATA_PATH), f"Processed features missing at {PROCESSED_DATA_PATH}"
    assert os.path.isfile(LOG_PATH), f"Server log missing at {LOG_PATH}"

def test_processed_features_format():
    with open(PROCESSED_DATA_PATH, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("Processed features file is empty")

        assert header == ["pc_1", "pc_2", "pc_3", "pc_4", "pc_5"], f"Incorrect header in processed features: {header}"

        rows = list(reader)
        assert len(rows) > 0, "Processed features file has no data rows"
        assert len(rows[0]) == 5, f"Processed features should have exactly 5 columns, got {len(rows[0])}"

        # Verify row count matches raw data
        with open(RAW_DATA_PATH, 'r') as rf:
            raw_reader = csv.reader(rf)
            raw_rows = list(raw_reader)
            # Subtract 1 for header
            assert len(rows) == len(raw_rows) - 1, "Processed features row count does not match raw features row count"

def test_health_endpoint():
    # Unauthorized
    try:
        resp_unauth = requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {BASE_URL}: {e}")

    assert resp_unauth.status_code == 401, f"Expected 401 for unauthorized /health, got {resp_unauth.status_code}"

    # Authorized
    resp_auth = requests.get(f"{BASE_URL}/health", headers=HEADERS, timeout=5)
    assert resp_auth.status_code == 200, f"Expected 200 for authorized /health, got {resp_auth.status_code}"

    try:
        data = resp_auth.json()
    except ValueError:
        pytest.fail(f"Invalid JSON response from /health: {resp_auth.text}")

    assert data == {"status": "ok"}, f"Unexpected response from /health: {data}"

def test_transform_endpoint():
    # Load raw data and compute expected PCA
    raw_data = np.loadtxt(RAW_DATA_PATH, delimiter=',', skiprows=1)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(raw_data)
    pca = PCA(n_components=5)
    pca.fit(scaled_data)

    # Test with zeros and another random point
    test_features = np.zeros(50)

    # Unauthorized
    resp_unauth = requests.post(
        f"{BASE_URL}/transform", 
        json={"features": test_features.tolist()},
        timeout=5
    )
    assert resp_unauth.status_code == 401, f"Expected 401 for unauthorized /transform, got {resp_unauth.status_code}"

    # Authorized
    resp_auth = requests.post(
        f"{BASE_URL}/transform", 
        headers=HEADERS,
        json={"features": test_features.tolist()},
        timeout=5
    )
    assert resp_auth.status_code == 200, f"Expected 200 for authorized /transform, got {resp_auth.status_code}"

    try:
        result = resp_auth.json()
    except ValueError:
        pytest.fail(f"Invalid JSON response from /transform: {resp_auth.text}")

    assert "reduced_features" in result, f"Response missing 'reduced_features': {result}"

    reduced = result["reduced_features"]
    assert len(reduced) == 5, f"Expected 5 reduced features, got {len(reduced)}"

    # Compute expected
    expected_reduced = pca.transform(scaler.transform([test_features]))[0]

    np.testing.assert_allclose(
        reduced, 
        expected_reduced, 
        rtol=1e-4, 
        atol=1e-4, 
        err_msg="Transformed features from API do not match expected PCA output"
    )