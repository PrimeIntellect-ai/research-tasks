# test_final_state.py

import os
import json
import pytest

def test_etl_pipeline_script_exists_and_executable():
    """Test that the ETL pipeline script exists and is executable."""
    script_path = "/home/user/etl_pipeline.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_virtual_environment_exists():
    """Test that the virtual environment was created."""
    venv_path = "/home/user/venv"
    assert os.path.exists(venv_path), f"The virtual environment directory {venv_path} does not exist."
    assert os.path.isdir(venv_path), f"The path {venv_path} is not a directory."
    python_bin = os.path.join(venv_path, "bin", "python")
    assert os.path.exists(python_bin), f"Python interpreter not found in virtual environment at {python_bin}."

def test_metrics_json_exists_and_correct():
    """Test that metrics.json exists, is valid JSON, and contains the correct metrics."""
    metrics_path = "/home/user/metrics.json"
    assert os.path.exists(metrics_path), f"The file {metrics_path} does not exist."
    assert os.path.isfile(metrics_path), f"The path {metrics_path} is not a file."

    with open(metrics_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {metrics_path} does not contain valid JSON.")

    expected_keys = {"mean", "ci_lower", "ci_upper"}
    assert set(metrics.keys()) == expected_keys, f"metrics.json keys {set(metrics.keys())} do not match expected {expected_keys}."

    assert isinstance(metrics["mean"], (int, float)), "mean must be a number."
    assert isinstance(metrics["ci_lower"], (int, float)), "ci_lower must be a number."
    assert isinstance(metrics["ci_upper"], (int, float)), "ci_upper must be a number."

    assert round(metrics["mean"], 2) == 49.48, f"Expected mean 49.48, got {metrics['mean']}."
    assert round(metrics["ci_lower"], 2) == 48.58, f"Expected ci_lower 48.58, got {metrics['ci_lower']}."
    assert round(metrics["ci_upper"], 2) == 50.38, f"Expected ci_upper 50.38, got {metrics['ci_upper']}."