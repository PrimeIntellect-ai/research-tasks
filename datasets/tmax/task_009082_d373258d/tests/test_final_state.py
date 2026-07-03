# test_final_state.py

import os
import json
import math
import pytest

def test_inference_plot_exists():
    plot_path = '/home/user/inference_plot.png'
    assert os.path.exists(plot_path), f"Expected plot file not found at {plot_path}"
    assert os.path.isfile(plot_path), f"Expected {plot_path} to be a file"
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty"

def test_pipeline_metrics_json():
    metrics_path = '/home/user/pipeline_metrics.json'
    assert os.path.exists(metrics_path), f"Expected metrics file not found at {metrics_path}"

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse {metrics_path} as JSON")

    assert "median_imputed" in metrics, "Missing 'median_imputed' in metrics JSON"
    assert "mean_prediction" in metrics, "Missing 'mean_prediction' in metrics JSON"
    assert "inference_time_seconds" in metrics, "Missing 'inference_time_seconds' in metrics JSON"

    # Assert values
    median_imputed = metrics["median_imputed"]
    mean_prediction = metrics["mean_prediction"]
    inference_time = metrics["inference_time_seconds"]

    assert isinstance(median_imputed, (int, float)), "'median_imputed' must be a number"
    assert isinstance(mean_prediction, (int, float)), "'mean_prediction' must be a number"
    assert isinstance(inference_time, (int, float)), "'inference_time_seconds' must be a number"

    # Check values with tolerance
    expected_median = -0.0617336
    expected_mean_pred = 10.84439

    assert math.isclose(median_imputed, expected_median, abs_tol=0.01), \
        f"Expected 'median_imputed' to be approx {expected_median}, got {median_imputed}"

    assert math.isclose(mean_prediction, expected_mean_pred, abs_tol=0.01), \
        f"Expected 'mean_prediction' to be approx {expected_mean_pred}, got {mean_prediction}"

    assert inference_time > 0, \
        f"Expected 'inference_time_seconds' to be > 0, got {inference_time}"