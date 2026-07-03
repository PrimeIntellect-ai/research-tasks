# test_final_state.py

import os
import pandas as pd

def test_etl_pipeline_accuracy():
    truth_path = "/tmp/truth.csv"
    pred_path = "/home/user/clean_metrics.csv"

    assert os.path.isfile(truth_path), f"Truth file missing: {truth_path}"
    assert os.path.isfile(pred_path), f"Output file missing: {pred_path}"

    try:
        truth_df = pd.read_csv(truth_path)
    except Exception as e:
        raise AssertionError(f"Failed to read truth file: {e}")

    try:
        pred_df = pd.read_csv(pred_path)
    except Exception as e:
        raise AssertionError(f"Failed to read output file: {e}")

    expected_cols = ['Timestamp', 'UserHash', 'NormalizedAction', 'MetricName', 'RollingAvg']

    assert list(pred_df.columns) == expected_cols, (
        f"Column mismatch. Expected {expected_cols}, got {list(pred_df.columns)}"
    )

    # Calculate Row Accuracy Percentage as specified in the verifier
    truth_records = set(tuple(x) for x in truth_df.to_numpy())
    pred_records = set(tuple(x) for x in pred_df.to_numpy())

    matches = len(truth_records.intersection(pred_records))
    accuracy = (matches / len(truth_df)) * 100

    assert accuracy >= 98.0, (
        f"Row match accuracy is {accuracy:.2f}%, which is less than the required threshold of 98.0%."
    )