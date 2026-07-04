# test_final_state.py
import os
import json
import pytest

def test_pipeline_saved():
    pipeline_path = '/home/user/output/pipeline.pkl'
    assert os.path.exists(pipeline_path), f"{pipeline_path} is missing."
    assert os.path.isfile(pipeline_path), f"{pipeline_path} is not a file."
    assert os.path.getsize(pipeline_path) > 0, f"{pipeline_path} is empty."

def test_metrics_saved():
    metrics_path = '/home/user/output/metrics.json'
    assert os.path.exists(metrics_path), f"{metrics_path} is missing."
    assert os.path.isfile(metrics_path), f"{metrics_path} is not a file."

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{metrics_path} does not contain valid JSON.")

    assert "accuracy" in metrics, "The key 'accuracy' is missing in metrics.json."
    accuracy = metrics["accuracy"]
    assert isinstance(accuracy, (float, int)), "The 'accuracy' value is not a number."
    assert 0.0 <= accuracy <= 1.0, f"The 'accuracy' value {accuracy} is out of bounds [0.0, 1.0]."