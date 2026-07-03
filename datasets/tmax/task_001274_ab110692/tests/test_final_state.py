# test_final_state.py

import os
import pandas as pd
from sklearn.metrics import mean_squared_error

def test_aggregated_404s_mse():
    pred_path = '/home/user/aggregated_404s.csv'
    truth_path = '/app/ground_truth.csv'

    assert os.path.exists(pred_path), f"Output file is missing: {pred_path}"
    assert os.path.exists(truth_path), f"Ground truth file is missing: {truth_path}"

    # Load data
    try:
        df_truth = pd.read_csv(truth_path, names=['ts', 'count']).set_index('ts')
    except Exception as e:
        raise AssertionError(f"Failed to read ground truth file {truth_path}: {e}")

    try:
        df_pred = pd.read_csv(pred_path, names=['ts', 'count']).set_index('ts')
    except Exception as e:
        raise AssertionError(f"Failed to read prediction file {pred_path}. Ensure it is a valid CSV with 'epoch_timestamp,404_count' format: {e}")

    # Align indices, fill missing with 0
    df_merged = df_truth.join(df_pred, how='outer', lsuffix='_true', rsuffix='_pred').fillna(0)

    # Compute MSE
    mse = mean_squared_error(df_merged['count_true'], df_merged['count_pred'])

    # Assert threshold
    assert mse <= 1.0, f"MSE {mse:.4f} exceeds threshold of 1.0. The aggregated counts do not closely match the reference."

def test_aggregator_tool_compiled():
    binary_path = "/app/vendored/window_agg/window_agg"
    assert os.path.exists(binary_path), f"Compiled aggregator tool is missing at {binary_path}. Did you fix the Makefile and run make?"
    assert os.access(binary_path, os.X_OK), f"The file at {binary_path} is not executable."