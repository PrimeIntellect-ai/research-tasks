# test_final_state.py
import os
import json
import pytest

def test_features_npy():
    try:
        import numpy as np
    except ImportError:
        pytest.fail("numpy is not installed but is required to verify features.npy")

    features_path = '/home/user/data/features.npy'
    assert os.path.exists(features_path), f"File {features_path} is missing"

    raw_data_path = '/home/user/data/raw.jsonl'
    assert os.path.exists(raw_data_path), f"Raw data file {raw_data_path} is missing"

    with open(raw_data_path, 'r') as f:
        num_rows = sum(1 for _ in f)

    features = np.load(features_path)
    expected_shape = (num_rows, 10)
    assert features.shape == expected_shape, f"Expected features shape {expected_shape}, got {features.shape}"

def test_models_exist():
    vectorizer_path = '/home/user/models/vectorizer.joblib'
    svd_path = '/home/user/models/svd.joblib'

    assert os.path.exists(vectorizer_path), f"Model file {vectorizer_path} is missing"
    assert os.path.exists(svd_path), f"Model file {svd_path} is missing"

def test_reproducibility_result():
    result_path = '/home/user/test_result.txt'
    assert os.path.exists(result_path), f"Result file {result_path} is missing"

    with open(result_path, 'r') as f:
        res = f.read().strip()

    assert res == "PASS", f"Reproducibility test failed, expected 'PASS' but got '{res}'"

def test_metrics_json():
    metrics_path = '/home/user/metrics.json'
    assert os.path.exists(metrics_path), f"Metrics file {metrics_path} is missing"

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metrics_path} does not contain valid JSON")

    assert 'num_runs' in metrics, "Key 'num_runs' is missing in metrics.json"
    assert metrics['num_runs'] == 50, f"Expected 'num_runs' to be 50, got {metrics['num_runs']}"

    assert 'avg_time_seconds' in metrics, "Key 'avg_time_seconds' is missing in metrics.json"
    assert isinstance(metrics['avg_time_seconds'], float) or isinstance(metrics['avg_time_seconds'], int), "avg_time_seconds must be a number"
    assert metrics['avg_time_seconds'] >= 0, "avg_time_seconds must be greater than or equal to 0"