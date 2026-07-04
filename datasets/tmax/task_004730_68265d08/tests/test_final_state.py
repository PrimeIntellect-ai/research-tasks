# test_final_state.py

import os
import json
import pytest

def test_metrics_json_exists():
    """Test that the metrics.json file exists in the correct location."""
    file_path = '/home/user/metrics.json'
    assert os.path.exists(file_path), f"The file {file_path} is missing. Did you forget to export the results?"
    assert os.path.isfile(file_path), f"The path {file_path} exists but is not a file."

def test_metrics_json_content():
    """Test that metrics.json contains the correct keys and values."""
    file_path = '/home/user/metrics.json'
    assert os.path.exists(file_path), "metrics.json not found."

    with open(file_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not a valid JSON file.")

    assert "reconstruction_mse" in results, "Key 'reconstruction_mse' missing from metrics.json"
    assert "anomaly_count" in results, "Key 'anomaly_count' missing from metrics.json"

    mse = results["reconstruction_mse"]
    anomaly_count = results["anomaly_count"]

    assert isinstance(mse, float), f"'reconstruction_mse' should be a float, got {type(mse)}"
    assert isinstance(anomaly_count, int), f"'anomaly_count' should be an int, got {type(anomaly_count)}"

    # Expected values based on the reproducible ground truth
    expected_mse = 0.8123
    expected_anomalies = 12

    assert abs(mse - expected_mse) < 0.0002, f"Expected reconstruction_mse to be close to {expected_mse}, got {mse}"
    assert anomaly_count == expected_anomalies, f"Expected anomaly_count to be {expected_anomalies}, got {anomaly_count}"