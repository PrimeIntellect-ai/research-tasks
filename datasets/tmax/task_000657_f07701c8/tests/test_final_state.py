# test_final_state.py
import os
import subprocess
import pytest

def test_predictions_mse():
    predictions_path = "/home/user/predictions.csv"
    test_data_path = "/app/data/test_sensors.csv"
    oracle_path = "/app/sensor_oracle"

    assert os.path.exists(predictions_path), f"Predictions file not found at {predictions_path}"
    assert os.path.exists(test_data_path), f"Test data file not found at {test_data_path}"
    assert os.path.exists(oracle_path), f"Oracle binary not found at {oracle_path}"

    # Generate ground truth
    result = subprocess.run([oracle_path, test_data_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Oracle failed to run on test data: {result.stderr}"

    truth_lines = [float(x) for x in result.stdout.strip().split('\n') if x]

    # Read predictions
    try:
        with open(predictions_path, 'r') as f:
            pred_lines = [float(x.strip()) for x in f.readlines() if x.strip()]
    except Exception as e:
        pytest.fail(f"Failed to read or parse predictions: {e}")

    assert len(truth_lines) == len(pred_lines), \
        f"Length mismatch: truth has {len(truth_lines)} rows, predictions have {len(pred_lines)} rows"

    mse = sum((t - p) ** 2 for t, p in zip(truth_lines, pred_lines)) / len(truth_lines)

    threshold = 0.01
    assert mse < threshold, f"MSE {mse} is not below the threshold of {threshold}"