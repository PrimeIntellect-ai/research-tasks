# test_final_state.py

import os
import pytest
import pandas as pd
import numpy as np

def test_pipeline_log_exists():
    """Verify that the pipeline log file was created."""
    log_path = '/home/user/pipeline.log'
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    assert os.path.getsize(log_path) > 0, f"Log file {log_path} is empty."

def test_telemetry_parquet_exists():
    """Verify that the output Parquet file was created."""
    parquet_path = '/home/user/telemetry.parquet'
    assert os.path.isfile(parquet_path), f"Output file {parquet_path} is missing."
    assert os.path.getsize(parquet_path) > 0, f"Output file {parquet_path} is empty."

def test_telemetry_schema():
    """Verify that the Parquet file has the correct schema."""
    parquet_path = '/home/user/telemetry.parquet'
    df = pd.read_parquet(parquet_path)

    expected_columns = {'frame_index', 'timestamp', 'signal'}
    actual_columns = set(df.columns)

    assert expected_columns.issubset(actual_columns), (
        f"Parquet file is missing expected columns. Expected {expected_columns}, found {actual_columns}."
    )

    # Check types
    assert pd.api.types.is_integer_dtype(df['frame_index']), "Column 'frame_index' must be an integer."
    assert pd.api.types.is_string_dtype(df['timestamp']) or pd.api.types.is_object_dtype(df['timestamp']), "Column 'timestamp' must be a string."
    assert pd.api.types.is_float_dtype(df['signal']) or pd.api.types.is_numeric_dtype(df['signal']), "Column 'signal' must be a float/numeric."

def test_telemetry_mse_metric():
    """Verify that the extracted signal has an MSE <= 5.0 compared to ground truth."""
    parquet_path = '/home/user/telemetry.parquet'
    gt_path = '/app/ground_truth.csv'

    assert os.path.isfile(parquet_path), f"Output file {parquet_path} missing."
    assert os.path.isfile(gt_path), f"Ground truth file {gt_path} missing."

    pred_df = pd.read_parquet(parquet_path)
    gt_df = pd.read_csv(gt_path)

    # Merge on frame_index
    merged = pd.merge(gt_df, pred_df, on='frame_index', suffixes=('_gt', '_pred'))

    assert len(merged) > 0, "No matching frames found between ground truth and predictions."
    assert len(merged) == len(gt_df), f"Expected {len(gt_df)} rows, but merged only {len(merged)} rows."

    # Calculate MSE
    mse = np.mean((merged['signal_gt'] - merged['signal_pred']) ** 2)

    threshold = 5.0
    assert mse <= threshold, f"MSE of {mse:.4f} exceeds the threshold of {threshold}. The extracted signal is not accurate enough."