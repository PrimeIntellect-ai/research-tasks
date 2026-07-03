# test_final_state.py
import os
import json
import pytest

def test_pipeline_saved():
    """Verify that the best pipeline was saved as a file."""
    pipeline_path = '/home/user/best_pipeline.pkl'
    assert os.path.exists(pipeline_path), f"Pipeline file not found at {pipeline_path}."
    assert os.path.isfile(pipeline_path), f"{pipeline_path} is not a regular file."
    assert os.path.getsize(pipeline_path) > 0, f"Pipeline file at {pipeline_path} is empty."

def test_metrics_json_saved_and_valid():
    """Verify that metrics.json exists and contains the correct structure."""
    metrics_path = '/home/user/metrics.json'
    assert os.path.exists(metrics_path), f"Metrics file not found at {metrics_path}."
    assert os.path.isfile(metrics_path), f"{metrics_path} is not a regular file."

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metrics_path} does not contain valid JSON.")

    assert "best_cv_score" in metrics, "Missing 'best_cv_score' key in metrics.json."
    assert "best_params" in metrics, "Missing 'best_params' key in metrics.json."

    score = metrics["best_cv_score"]
    assert isinstance(score, (float, int)), "best_cv_score must be a numeric value."
    assert 0.0 <= score <= 1.0, f"best_cv_score ({score}) is out of expected bounds [0.0, 1.0]."

    params = metrics["best_params"]
    assert isinstance(params, dict), "best_params must be a dictionary object."

    keys_str = str(params.keys())
    assert "n_estimators" in keys_str, "n_estimators parameter is missing from best_params."
    assert "max_depth" in keys_str, "max_depth parameter is missing from best_params."