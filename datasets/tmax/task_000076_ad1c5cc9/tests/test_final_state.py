# test_final_state.py

import os
import pandas as pd
import pytest

def test_anomalies_f1_score():
    """
    Validates that the output anomalies file exists, has the correct structure,
    and achieves an F1 score >= 0.95 compared to the ground truth.
    """
    pred_path = '/home/user/anomalies.csv'
    truth_path = '/app/ground_truth_anomalies.csv'

    assert os.path.exists(pred_path), f"The output file was not found at {pred_path}"
    assert os.path.exists(truth_path), f"The ground truth file was not found at {truth_path}"

    try:
        pred_df = pd.read_csv(pred_path)
    except Exception as e:
        pytest.fail(f"Failed to read {pred_path} as CSV: {e}")

    try:
        truth_df = pd.read_csv(truth_path)
    except Exception as e:
        pytest.fail(f"Failed to read {truth_path} as CSV: {e}")

    assert 'bucket_start_timestamp' in pred_df.columns, (
        f"The output file is missing the 'bucket_start_timestamp' column. "
        f"Found columns: {list(pred_df.columns)}"
    )

    try:
        truth_set = set(truth_df['bucket_start_timestamp'].astype(int))
        pred_set = set(pred_df['bucket_start_timestamp'].astype(int))
    except ValueError as e:
        pytest.fail(f"Could not convert 'bucket_start_timestamp' to integers: {e}")

    # Calculate true positives, false positives, false negatives
    tp = len(truth_set.intersection(pred_set))
    fp = len(pred_set - truth_set)
    fn = len(truth_set - pred_set)

    if tp + fp == 0:
        precision = 0.0
    else:
        precision = tp / (tp + fp)

    if tp + fn == 0:
        recall = 0.0
    else:
        recall = tp / (tp + fn)

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, (
        f"F1 Score {f1:.4f} is below the threshold of 0.95. "
        f"(Precision: {precision:.4f}, Recall: {recall:.4f}, TP: {tp}, FP: {fp}, FN: {fn})"
    )