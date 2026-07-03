# test_final_state.py

import os
import json
import pytest

def test_fit_plot_exists():
    """Verify that the experimental data visualization plot was created."""
    plot_path = "/home/user/fit_plot.png"
    assert os.path.isfile(plot_path), f"Visualization plot not found at {plot_path}."
    assert os.path.getsize(plot_path) > 0, "Visualization plot file is empty."

def test_analysis_results_json():
    """Verify that the analysis results JSON exists, has correct keys, and expected values."""
    json_path = "/home/user/analysis_results.json"
    assert os.path.isfile(json_path), f"Results JSON not found at {json_path}."

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON file {json_path}: {e}")

    expected_keys = {"valid_trials_count", "mean_k", "ks_statistic", "ttest_pvalue"}
    actual_keys = set(results.keys())
    assert expected_keys.issubset(actual_keys), f"JSON is missing keys. Expected {expected_keys}, found {actual_keys}."

    # Check valid_trials_count
    valid_trials = results.get("valid_trials_count")
    assert isinstance(valid_trials, int), f"'valid_trials_count' must be an integer, got {type(valid_trials)}."
    assert valid_trials == 80, f"Expected 80 valid trials, got {valid_trials}."

    # Check mean_k
    mean_k = results.get("mean_k")
    assert isinstance(mean_k, (int, float)), f"'mean_k' must be a float, got {type(mean_k)}."
    assert 0.54 < mean_k < 0.57, f"'mean_k' out of expected bounds (0.54, 0.57): {mean_k}"

    # Check ks_statistic
    ks_stat = results.get("ks_statistic")
    assert isinstance(ks_stat, (int, float)), f"'ks_statistic' must be a float, got {type(ks_stat)}."
    assert 0.05 < ks_stat < 0.08, f"'ks_statistic' out of expected bounds (0.05, 0.08): {ks_stat}"

    # Check ttest_pvalue
    pvalue = results.get("ttest_pvalue")
    assert isinstance(pvalue, (int, float)), f"'ttest_pvalue' must be a float, got {type(pvalue)}."
    assert pvalue < 0.01, f"'ttest_pvalue' out of expected bounds (< 0.01): {pvalue}"