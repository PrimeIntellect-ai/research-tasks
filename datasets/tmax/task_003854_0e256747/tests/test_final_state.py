# test_final_state.py

import os
import pandas as pd
import pytest

def test_results_csv_exists():
    """Check that the results file was created at the expected path."""
    path = "/home/user/results.csv"
    assert os.path.exists(path), f"Output file {path} is missing."
    assert os.path.isfile(path), f"Output path {path} is not a file."

def test_results_accuracy():
    """Verify the accuracy of the Naive Bayes probabilities using MSE."""
    pred_path = "/home/user/results.csv"
    truth_path = "/tmp/golden_results.csv"

    assert os.path.exists(pred_path), f"Prediction file not found at {pred_path}"
    assert os.path.exists(truth_path), f"Golden reference file not found at {truth_path}"

    try:
        pred = pd.read_csv(pred_path)
    except Exception as e:
        pytest.fail(f"Failed to read {pred_path} as CSV: {e}")

    try:
        truth = pd.read_csv(truth_path)
    except Exception as e:
        pytest.fail(f"Failed to read {truth_path} as CSV: {e}")

    assert 'user_id' in pred.columns, "The output file is missing the 'user_id' column."
    assert 'prob_1' in pred.columns, "The output file is missing the 'prob_1' column."

    assert len(pred) == len(truth), f"Row count mismatch: expected {len(truth)} rows, got {len(pred)}."

    # Check that user_id matches and is sorted correctly
    if not (pred['user_id'] == truth['user_id']).all():
        pytest.fail("The 'user_id' column in results.csv does not match the expected values or is out of order.")

    # Calculate Mean Squared Error
    mse = ((pred['prob_1'] - truth['prob_1']) ** 2).mean()
    threshold = 1e-6

    assert mse <= threshold, f"Calculated MSE of {mse:.8e} exceeds the maximum allowed threshold of {threshold:.8e}. The model probabilities are not accurate enough."