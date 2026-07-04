# test_final_state.py

import os
import numpy as np
import pytest

def test_predictions_file_exists():
    path = "/home/user/predictions.txt"
    assert os.path.isfile(path), f"The predictions file is missing at {path}."

def test_mse_metric_threshold():
    preds_path = "/home/user/predictions.txt"
    truth_path = "/home/user/data/test_targets_hidden.csv"

    assert os.path.isfile(preds_path), f"Cannot evaluate MSE: {preds_path} does not exist."
    assert os.path.isfile(truth_path), f"Cannot evaluate MSE: {truth_path} does not exist."

    try:
        preds = np.loadtxt(preds_path)
    except Exception as e:
        pytest.fail(f"Failed to load predictions from {preds_path}. Ensure it contains one floating-point prediction per line. Error: {e}")

    try:
        truth = np.loadtxt(truth_path)
    except Exception as e:
        pytest.fail(f"Failed to load truth targets from {truth_path}: {e}")

    assert preds.shape == truth.shape, (
        f"Shape mismatch: predictions have shape {preds.shape}, "
        f"but the test set has {truth.shape[0]} rows."
    )

    mse = np.mean((preds - truth) ** 2)
    threshold = 2.5

    assert mse <= threshold, (
        f"MSE threshold not met. "
        f"Measured MSE: {mse:.4f}, but required MSE <= {threshold}."
    )