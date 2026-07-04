# test_final_state.py

import os
import json
import pytest
from sklearn.metrics import mean_squared_error

def test_process_network_script_exists():
    path = "/home/user/process_network.py"
    assert os.path.isfile(path), f"The script {path} does not exist. You must create it to automate the pipeline."

def test_final_metrics_json_exists():
    path = "/home/user/final_metrics.json"
    assert os.path.isfile(path), f"The output file {path} does not exist."

def test_final_metrics_accuracy():
    pred_path = "/home/user/final_metrics.json"
    truth_path = "/app/ground_truth.json"

    assert os.path.isfile(pred_path), f"Missing predictions file at {pred_path}"
    assert os.path.isfile(truth_path), f"Missing ground truth file at {truth_path}"

    with open(pred_path, 'r') as f:
        try:
            pred = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {pred_path} is not valid JSON.")

    with open(truth_path, 'r') as f:
        truth = json.load(f)

    common_keys = set(pred.keys()).intersection(set(truth.keys()))

    assert len(truth) > 0, "Ground truth JSON is empty."

    coverage = len(common_keys) / len(truth)
    assert coverage >= 0.9, f"Missing too many keys. Found {len(common_keys)} out of {len(truth)} expected keys (coverage: {coverage:.2%})."

    y_true = [truth[k] for k in common_keys]
    y_pred = [pred[k] for k in common_keys]

    mse = mean_squared_error(y_true, y_pred)
    threshold = 0.0001

    assert mse <= threshold, f"Calculated MSE {mse:.6f} is greater than the threshold {threshold}. Your graph metrics are not accurate enough."