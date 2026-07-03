# test_final_state.py
import os
import json
import pytest

def test_requirements_file_exists():
    """Test that the requirements.txt file was created."""
    req_file = "/home/user/pipeline/requirements.txt"
    assert os.path.isfile(req_file), f"Requirements file missing: {req_file}"

def test_artifacts_exist():
    """Test that the model and metrics artifacts were generated."""
    model_file = "/home/user/artifacts/model.pkl"
    metrics_file = "/home/user/artifacts/metrics.json"

    assert os.path.isfile(model_file), f"Model artifact missing: {model_file}"
    assert os.path.isfile(metrics_file), f"Metrics artifact missing: {metrics_file}"

def test_metrics_values():
    """Test that the metrics.json contains the correct mse and r2 values."""
    metrics_file = "/home/user/artifacts/metrics.json"

    with open(metrics_file, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Metrics file {metrics_file} is not valid JSON.")

    assert "mse" in metrics, "Key 'mse' missing in metrics.json"
    assert "r2" in metrics, "Key 'r2' missing in metrics.json"

    mse = metrics["mse"]
    r2 = metrics["r2"]

    assert isinstance(mse, (float, int)), f"'mse' should be a float, got {type(mse)}"
    assert isinstance(r2, (float, int)), f"'r2' should be a float, got {type(r2)}"

    expected_mse = 0.2338
    expected_r2 = 0.9856

    assert abs(float(mse) - expected_mse) < 0.01, f"MSE {mse} is not within 0.01 of expected {expected_mse}"
    assert abs(float(r2) - expected_r2) < 0.01, f"R2 {r2} is not within 0.01 of expected {expected_r2}"