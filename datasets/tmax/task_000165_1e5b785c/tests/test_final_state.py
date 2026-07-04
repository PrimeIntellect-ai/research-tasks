# test_final_state.py

import os
import json
import numpy as np
import pytest

def calculate_mse(reference_json_path, predicted_json_path):
    with open(reference_json_path, 'r') as f:
        y_true = np.array(json.load(f))
    try:
        with open(predicted_json_path, 'r') as f:
            y_pred = np.array(json.load(f))
    except Exception as e:
        return 9999.0

    if len(y_true) != len(y_pred):
        min_len = min(len(y_true), len(y_pred))
        mse = np.mean((y_true[:min_len] - y_pred[:min_len])**2)
        mse += abs(len(y_true) - len(y_pred)) * 1.0 # Heavy penalty
        return float(mse)

    return float(np.mean((y_true - y_pred)**2))

def test_run_test_sh_exists():
    path = "/home/user/run_test.sh"
    assert os.path.isfile(path), f"Integration test script {path} does not exist."

def test_output_json_exists():
    path = "/home/user/output.json"
    assert os.path.isfile(path), f"Output file {path} does not exist."

def test_envelope_mse_metric():
    ref_path = "/root/reference_envelope.json"
    pred_path = "/home/user/output.json"

    assert os.path.isfile(ref_path), f"Reference file {ref_path} missing. Environment setup issue."
    assert os.path.isfile(pred_path), f"Predicted file {pred_path} missing."

    mse = calculate_mse(ref_path, pred_path)
    threshold = 0.001

    assert mse <= threshold, f"MSE {mse} exceeds threshold {threshold}. Output array does not match the reference envelope."