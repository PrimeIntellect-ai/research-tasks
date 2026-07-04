# test_final_state.py

import os
import json
import math
import pytest

def test_model_metrics_json_exists():
    """Check if the model_metrics.json file is created."""
    file_path = '/home/user/model_metrics.json'
    assert os.path.exists(file_path), f"The file {file_path} does not exist. Did you save the output?"
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_model_metrics_json_content():
    """Check if the model_metrics.json file contains the correct structure and values."""
    file_path = '/home/user/model_metrics.json'

    with open(file_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} is not valid JSON.")

    assert "best_alpha" in metrics, "The key 'best_alpha' is missing from the JSON file."
    assert "r2_score" in metrics, "The key 'r2_score' is missing from the JSON file."

    # Check best_alpha
    expected_alpha = 10.0
    actual_alpha = metrics["best_alpha"]
    assert isinstance(actual_alpha, (int, float)), "'best_alpha' must be a number."
    assert math.isclose(actual_alpha, expected_alpha, rel_tol=1e-4), \
        f"Expected best_alpha to be {expected_alpha}, got {actual_alpha}. Check your cross-validation setup."

    # Check r2_score
    expected_r2 = 0.9928
    actual_r2 = metrics["r2_score"]
    assert isinstance(actual_r2, (int, float)), "'r2_score' must be a number."
    assert math.isclose(actual_r2, expected_r2, abs_tol=1e-2), \
        f"Expected r2_score to be approximately {expected_r2}, got {actual_r2}. Check your data filtering and random seed."