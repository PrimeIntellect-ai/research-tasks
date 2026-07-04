# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_predictions_mse():
    pred_path = "/home/user/predictions.csv"
    truth_path = "/app/ground_truth.csv"

    assert os.path.exists(pred_path), f"Predictions file not found at {pred_path}"
    assert os.path.exists(truth_path), f"Ground truth file not found at {truth_path}"

    try:
        pred_df = pd.read_csv(pred_path)
    except Exception as e:
        pytest.fail(f"Could not read {pred_path} as CSV: {e}")

    try:
        truth_df = pd.read_csv(truth_path)
    except Exception as e:
        pytest.fail(f"Could not read {truth_path} as CSV: {e}")

    assert "id" in pred_df.columns, "Predictions must contain an 'id' column"
    assert "probability_class_1" in pred_df.columns, "Predictions must contain a 'probability_class_1' column"

    merged = pd.merge(truth_df, pred_df, on="id", suffixes=('_true', '_pred'))
    assert len(merged) > 0, "No matching IDs found between predictions and ground truth"

    mse = np.mean((merged['probability_class_1_true'] - merged['probability_class_1_pred'])**2)

    assert mse <= 0.0001, f"MSE is {mse:.6f}, which is greater than the threshold of 0.0001"

def test_c_file_exists():
    c_file = "/home/user/naive_bayes.c"
    assert os.path.exists(c_file), f"C source file not found at {c_file}"