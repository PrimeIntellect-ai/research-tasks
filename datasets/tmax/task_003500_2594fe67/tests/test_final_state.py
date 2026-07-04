# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_pipeline_files_exist():
    """Check that the expected intermediate and source files exist."""
    assert os.path.exists('/home/user/frame_stats.csv'), "The frame_stats.csv file is missing."
    assert os.path.exists('/home/user/pipeline.cpp'), "The pipeline.cpp source file is missing."
    assert os.path.exists('/home/user/pipeline'), "The compiled pipeline executable is missing."

def test_predictions_exist():
    """Check that the predictions CSV file was generated."""
    assert os.path.exists('/home/user/predictions.csv'), "The predictions.csv file is missing."

def test_mse_metric():
    """Evaluate the predictions against the MSE threshold."""
    pred_path = '/home/user/predictions.csv'
    assert os.path.exists(pred_path), f"File not found: {pred_path}"

    try:
        df = pd.read_csv(pred_path)
    except Exception as e:
        pytest.fail(f"Failed to read {pred_path}: {e}")

    required_cols = {'frame_index', 'actual_target', 'predicted_target'}
    assert required_cols.issubset(df.columns), f"Missing columns in predictions.csv. Expected {required_cols}, found {set(df.columns)}"

    # Calculate Mean Squared Error
    mse = np.mean((df['actual_target'] - df['predicted_target'])**2)
    threshold = 0.05

    assert mse <= threshold, f"FAIL: MSE {mse:.4f} > {threshold}"