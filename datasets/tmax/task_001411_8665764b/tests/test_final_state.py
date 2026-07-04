# test_final_state.py

import os
import json
import pytest

def test_scripts_exist():
    """Verify that the required scripts have been created."""
    pipeline_path = '/home/user/pipeline.py'
    shell_script_path = '/home/user/run_pipeline.sh'

    assert os.path.isfile(pipeline_path), f"Python script {pipeline_path} is missing."
    assert os.path.isfile(shell_script_path), f"Shell script {shell_script_path} is missing."
    assert os.access(shell_script_path, os.X_OK), f"Shell script {shell_script_path} is not executable."

def test_metrics_json_exists_and_correct():
    """Verify that metrics.json exists and contains the correct computed metrics."""
    metrics_path = '/home/user/metrics.json'
    assert os.path.isfile(metrics_path), f"Output file {metrics_path} is missing."

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metrics_path} does not contain valid JSON.")

    expected_metrics = {
        "total_rows": 3,
        "total_tokens": 32,
        "total_cost": 0.0064
    }

    assert "total_rows" in metrics, "Key 'total_rows' is missing from metrics.json."
    assert "total_tokens" in metrics, "Key 'total_tokens' is missing from metrics.json."
    assert "total_cost" in metrics, "Key 'total_cost' is missing from metrics.json."

    assert metrics["total_rows"] == expected_metrics["total_rows"], \
        f"Expected total_rows to be {expected_metrics['total_rows']}, got {metrics['total_rows']}."

    assert metrics["total_tokens"] == expected_metrics["total_tokens"], \
        f"Expected total_tokens to be {expected_metrics['total_tokens']}, got {metrics['total_tokens']}."

    assert metrics["total_cost"] == expected_metrics["total_cost"], \
        f"Expected total_cost to be {expected_metrics['total_cost']}, got {metrics['total_cost']}."