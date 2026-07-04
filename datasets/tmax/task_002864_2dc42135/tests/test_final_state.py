# test_final_state.py

import os
import numpy as np
import pandas as pd
import pytest

def test_predictions_file_exists():
    """Check that the predictions file was created at the correct location."""
    pred_path = '/home/user/predictions.csv'
    assert os.path.exists(pred_path), f"Predictions file not found at {pred_path}"
    assert os.path.isfile(pred_path), f"Expected {pred_path} to be a file"

def test_predictions_mse_threshold():
    """Verify that the predictions match the ground truth with an MSE <= 0.1."""
    pred_path = '/home/user/predictions.csv'
    truth_path = '/tmp/true_test_scores.csv'

    assert os.path.exists(pred_path), "Cannot check MSE because predictions file is missing."
    assert os.path.exists(truth_path), "Ground truth file is missing (internal error)."

    try:
        preds = pd.read_csv(pred_path, header=None).values.flatten()
    except Exception as e:
        pytest.fail(f"Failed to read predictions file {pred_path}: {e}")

    try:
        truth = pd.read_csv(truth_path, header=None).values.flatten()
    except Exception as e:
        pytest.fail(f"Failed to read ground truth file {truth_path}: {e}")

    assert len(preds) == len(truth), f"Length mismatch: predictions has {len(preds)} rows, expected {len(truth)}."

    # Compute the Mean Squared Error (MSE)
    mse = np.mean((preds - truth)**2)

    # Assert against the threshold
    assert mse <= 0.1, f"MSE is too high. Expected <= 0.1, but got {mse:.4f}"