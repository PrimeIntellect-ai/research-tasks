# test_final_state.py

import os
import pandas as pd
from sklearn.metrics import mean_squared_error
import pytest

def test_results_csv_exists():
    """Verify that the user generated the results.csv file."""
    results_path = '/home/user/results.csv'
    assert os.path.isfile(results_path), f"Expected output file not found: {results_path}"

def test_results_mse():
    """Verify that the Mean Squared Error of the rolling_bytes column is 0.0."""
    results_path = '/home/user/results.csv'
    gt_path = '/tmp/ground_truth_results.csv'

    assert os.path.isfile(results_path), f"Expected output file not found: {results_path}"
    assert os.path.isfile(gt_path), f"Ground truth file missing: {gt_path}"

    try:
        df_pred = pd.read_csv(results_path)
    except Exception as e:
        pytest.fail(f"Failed to read {results_path}: {e}")

    try:
        df_gt = pd.read_csv(gt_path)
    except Exception as e:
        pytest.fail(f"Failed to read {gt_path}: {e}")

    # Check if required columns exist in predictions
    required_columns = ['frame_id', 'destination', 'rolling_bytes']
    for col in required_columns:
        assert col in df_pred.columns, f"Missing required column '{col}' in {results_path}"

    df_pred = df_pred.sort_values(by=['frame_id', 'destination']).reset_index(drop=True)
    df_gt = df_gt.sort_values(by=['frame_id', 'destination']).reset_index(drop=True)

    assert len(df_pred) == len(df_gt), f"Row count mismatch: expected {len(df_gt)} rows, found {len(df_pred)} rows."

    mse = mean_squared_error(df_gt['rolling_bytes'], df_pred['rolling_bytes'])

    assert mse <= 0.0, f"MSE of rolling_bytes is {mse}, but threshold is <= 0.0"

def test_cypher_query_exists():
    """Verify that the user generated the rolling_query.cypher file."""
    cypher_path = '/home/user/rolling_query.cypher'
    assert os.path.isfile(cypher_path), f"Expected Cypher query file not found: {cypher_path}"
    assert os.path.getsize(cypher_path) > 0, f"Cypher query file {cypher_path} is empty."