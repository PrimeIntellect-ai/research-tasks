# test_final_state.py

import os
import pandas as pd
import pytest

def test_predictions_exist():
    predictions_path = '/home/user/predictions.csv'
    assert os.path.exists(predictions_path), f"Predictions file not found at {predictions_path}"
    assert os.path.isfile(predictions_path), f"Expected {predictions_path} to be a file"

def test_predictions_mse():
    predictions_path = '/home/user/predictions.csv'
    truth_path = '/app/test_truth.csv'

    assert os.path.exists(predictions_path), f"Predictions file not found at {predictions_path}"
    assert os.path.exists(truth_path), f"Truth file not found at {truth_path}"

    try:
        pred_df = pd.read_csv(predictions_path)
    except Exception as e:
        pytest.fail(f"Failed to read {predictions_path}: {e}")

    try:
        true_df = pd.read_csv(truth_path)
    except Exception as e:
        pytest.fail(f"Failed to read {truth_path}: {e}")

    assert 'id' in pred_df.columns, f"Column 'id' not found in predictions.csv. Found: {list(pred_df.columns)}"
    assert 'Y_pred' in pred_df.columns, f"Column 'Y_pred' not found in predictions.csv. Found: {list(pred_df.columns)}"

    merged = pd.merge(true_df, pred_df, on='id', how='inner')

    assert len(merged) == len(true_df), f"Expected {len(true_df)} predictions, but found {len(merged)} matching ids."

    mse = ((merged['Y_true'] - merged['Y_pred']) ** 2).mean()

    threshold = 2.0
    assert mse <= threshold, f"MSE is {mse:.4f}, which is greater than the threshold of {threshold}"