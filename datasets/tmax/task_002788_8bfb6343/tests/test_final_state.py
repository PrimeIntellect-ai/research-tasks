# test_final_state.py
import os
import pandas as pd
import numpy as np
import pytest

def test_processed_signal_exists():
    """Check if the agent correctly created the output file."""
    assert os.path.isfile('/home/user/processed_signal.csv'), "The output file /home/user/processed_signal.csv was not found."

def test_processed_signal_mse():
    """Verify that the mean squared error of the processed signal is within the acceptable threshold."""
    gt_path = '/app/ground_truth.csv'
    pred_path = '/home/user/processed_signal.csv'

    assert os.path.isfile(gt_path), f"Ground truth file {gt_path} is missing."
    assert os.path.isfile(pred_path), f"Prediction file {pred_path} is missing."

    try:
        gt = pd.read_csv(gt_path, header=None)
    except Exception as e:
        pytest.fail(f"Failed to read {gt_path}: {e}")

    try:
        pred = pd.read_csv(pred_path, header=None)
    except Exception as e:
        pytest.fail(f"Failed to read {pred_path}: {e}")

    assert len(gt) == len(pred), f"Length mismatch: expected {len(gt)} rows, but got {len(pred)} rows."

    assert len(pred.columns) >= 2, f"Expected at least 2 columns in {pred_path}, found {len(pred.columns)}."

    # Calculate MSE between the second columns
    mse = np.mean((gt.iloc[:, 1] - pred.iloc[:, 1])**2)

    assert mse <= 1e-5, f"MSE {mse:.8f} exceeds threshold of 1e-5. The output values do not match the expected smoothed normalized amplitude closely enough."