# test_final_state.py

import os
import json
import pytest

def test_etl_pipeline_script_exists():
    """Test that the ETL pipeline script exists."""
    script_path = "/home/user/etl_pipeline.py"
    assert os.path.exists(script_path), f"The script {script_path} is missing."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_metrics_json_exists_and_format():
    """Test that metrics.json exists, is valid JSON, and contains the accuracy key."""
    metrics_path = "/home/user/metrics.json"
    assert os.path.exists(metrics_path), f"The file {metrics_path} is missing. Did the script run and produce it?"
    assert os.path.isfile(metrics_path), f"The path {metrics_path} is not a file."

    with open(metrics_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {metrics_path} does not contain valid JSON.")

    assert "accuracy" in data, f"The key 'accuracy' is missing from {metrics_path}."

    accuracy = data["accuracy"]
    assert isinstance(accuracy, (float, int)), f"The 'accuracy' value should be a number, got {type(accuracy).__name__}."
    assert 0.0 <= accuracy <= 1.0, f"The 'accuracy' value should be between 0.0 and 1.0, got {accuracy}."