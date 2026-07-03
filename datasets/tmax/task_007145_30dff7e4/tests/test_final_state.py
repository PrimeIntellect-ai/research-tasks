# test_final_state.py

import os
import json
import pytest

def test_experiment_log_exists():
    """Test that the experiment log file exists."""
    log_path = '/home/user/experiment_log.json'
    assert os.path.isfile(log_path), f"Experiment log file is missing at {log_path}"

def test_experiment_log_content():
    """Test that the experiment log file contains the correct results."""
    log_path = '/home/user/experiment_log.json'

    with open(log_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {log_path} is not valid JSON.")

    assert "top_3_outlier_ids" in data, "Key 'top_3_outlier_ids' is missing from the JSON file."
    assert "mean_absolute_error" in data, "Key 'mean_absolute_error' is missing from the JSON file."

    expected_outliers = [13, 46, 89]
    assert data["top_3_outlier_ids"] == expected_outliers, \
        f"Expected top_3_outlier_ids to be {expected_outliers}, but got {data['top_3_outlier_ids']}"

    expected_mae = 1.5583
    actual_mae = data["mean_absolute_error"]
    assert isinstance(actual_mae, (int, float)), "mean_absolute_error must be a number."
    assert abs(actual_mae - expected_mae) <= 0.0001, \
        f"Expected mean_absolute_error to be approximately {expected_mae}, but got {actual_mae}"