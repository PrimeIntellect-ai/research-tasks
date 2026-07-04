# test_final_state.py

import os
import json
import math
import pytest

def test_pipeline_results_exists():
    """Verify that the pipeline_results.json file was created."""
    file_path = "/home/user/pipeline_results.json"
    assert os.path.exists(file_path), f"The results file is missing at {file_path}."
    assert os.path.isfile(file_path), f"The path {file_path} exists but is not a file."

def test_pipeline_results_content():
    """Verify the contents of the pipeline_results.json file."""
    file_path = "/home/user/pipeline_results.json"

    with open(file_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    expected_keys = {"balanced_rows", "explained_variance_sum", "roc_auc"}
    actual_keys = set(results.keys())

    assert expected_keys.issubset(actual_keys), f"Missing keys in JSON. Expected {expected_keys}, found {actual_keys}."

    # Check balanced_rows
    assert isinstance(results["balanced_rows"], int), "'balanced_rows' must be an integer."
    assert results["balanced_rows"] == 1900, f"Expected 'balanced_rows' to be 1900, got {results['balanced_rows']}."

    # Check explained_variance_sum
    assert isinstance(results["explained_variance_sum"], (float, int)), "'explained_variance_sum' must be a float."
    expected_var_sum = 0.1585
    assert math.isclose(results["explained_variance_sum"], expected_var_sum, abs_tol=0.005), \
        f"Expected 'explained_variance_sum' to be approx {expected_var_sum}, got {results['explained_variance_sum']}."

    # Check roc_auc
    assert isinstance(results["roc_auc"], (float, int)), "'roc_auc' must be a float."
    expected_auc = 0.9427
    assert math.isclose(results["roc_auc"], expected_auc, abs_tol=0.005), \
        f"Expected 'roc_auc' to be approx {expected_auc}, got {results['roc_auc']}."