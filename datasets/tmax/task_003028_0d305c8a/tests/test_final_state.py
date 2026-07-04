# test_final_state.py
import os
import json
import pytest
import urllib.request
import sqlite3
import yaml

WORKSPACE_DIR = "/home/user/workspace"
JSON_PATH = os.path.join(WORKSPACE_DIR, "ci_results.json")
MLRUNS_DIR = os.path.join(WORKSPACE_DIR, "mlruns")

def test_json_results_exist_and_format():
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} does not exist. Did you save the JSON file?"

    with open(JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("ci_results.json is not a valid JSON file.")

    assert "ci_lower" in data, "JSON missing 'ci_lower' key."
    assert "ci_upper" in data, "JSON missing 'ci_upper' key."

    assert isinstance(data["ci_lower"], (int, float)), "'ci_lower' must be a number."
    assert isinstance(data["ci_upper"], (int, float)), "'ci_upper' must be a number."

def test_mlflow_experiment_exists():
    assert os.path.isdir(MLRUNS_DIR), "mlruns directory not found. Did you run MLflow tracking?"

    experiment_found = False

    # MLflow might use file-based storage
    for root, dirs, files in os.walk(MLRUNS_DIR):
        if "meta.yaml" in files:
            with open(os.path.join(root, "meta.yaml"), "r") as f:
                content = f.read()
                if "name: text_classification_fixed" in content:
                    experiment_found = True
                    break

    assert experiment_found, "Could not find MLflow experiment named 'text_classification_fixed' in mlruns."

def test_mlflow_metrics_logged():
    # Find the experiment ID
    exp_id = None
    for root, dirs, files in os.walk(MLRUNS_DIR):
        if "meta.yaml" in files:
            with open(os.path.join(root, "meta.yaml"), "r") as f:
                content = f.read()
                if "name: text_classification_fixed" in content:
                    # The folder name is usually the experiment ID
                    exp_id = os.path.basename(root)
                    break

    if not exp_id:
        pytest.fail("Experiment 'text_classification_fixed' not found.")

    # Check runs inside this experiment
    exp_dir = os.path.join(MLRUNS_DIR, exp_id)
    runs = [d for d in os.listdir(exp_dir) if os.path.isdir(os.path.join(exp_dir, d)) and d != "tags"]

    assert len(runs) > 0, "No runs found for the experiment 'text_classification_fixed'."

    # Check metrics in the latest run
    run_dir = os.path.join(exp_dir, runs[0])
    metrics_dir = os.path.join(run_dir, "metrics")

    assert os.path.isdir(metrics_dir), "Metrics directory not found in the MLflow run."

    logged_metrics = os.listdir(metrics_dir)
    assert "cv_mean" in logged_metrics, "'cv_mean' metric was not logged to MLflow."
    assert "ci_lower" in logged_metrics, "'ci_lower' metric was not logged to MLflow."
    assert "ci_upper" in logged_metrics, "'ci_upper' metric was not logged to MLflow."