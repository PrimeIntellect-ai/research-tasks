# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_final_output_exists():
    pred_path = '/home/user/final_output.csv'
    assert os.path.isfile(pred_path), f"The final output file {pred_path} was not generated."

def test_metrics_threshold():
    gt_path = '/app/ground_truth.csv'
    pred_path = '/home/user/final_output.csv'

    assert os.path.isfile(gt_path), f"Ground truth file {gt_path} is missing."
    assert os.path.isfile(pred_path), f"Prediction file {pred_path} is missing."

    try:
        gt = pd.read_csv(gt_path)
    except Exception as e:
        pytest.fail(f"Failed to read ground truth CSV: {e}")

    try:
        pred = pd.read_csv(pred_path)
    except Exception as e:
        pytest.fail(f"Failed to read prediction CSV: {e}")

    assert len(gt) == len(pred), f"Length mismatch: Expected {len(gt)} rows, but got {len(pred)} rows in final_output.csv."

    assert 'calibrated_threshold' in pred.columns, "Column 'calibrated_threshold' missing in final_output.csv."
    assert 'event_count' in pred.columns, "Column 'event_count' missing in final_output.csv."

    # Calculate metrics
    mse_threshold = np.mean((gt['calibrated_threshold'] - pred['calibrated_threshold'])**2)
    acc_events = np.mean(gt['event_count'] == pred['event_count'])

    # Assert against thresholds
    assert mse_threshold <= 2.0, f"MSE for calibrated_threshold is {mse_threshold:.3f}, which is > 2.0 threshold."
    assert acc_events >= 0.95, f"Event count accuracy is {acc_events:.3f}, which is < 0.95 threshold."

def test_recovered_script_exists():
    script_path = '/home/user/pipeline/process_log.awk'
    assert os.path.isfile(script_path), f"The deleted script was not recovered to {script_path}."