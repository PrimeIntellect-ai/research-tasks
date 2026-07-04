# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import math
import csv
import pytest

def test_fix_summary_exists_and_valid():
    summary_path = "/home/user/pipeline/fix_summary.json"
    assert os.path.isfile(summary_path), f"File {summary_path} does not exist."

    with open(summary_path, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("fix_summary.json is not a valid JSON file.")

    assert "run_id" in summary, "run_id missing from fix_summary.json"
    assert "mse_ci_lower" in summary, "mse_ci_lower missing from fix_summary.json"
    assert "mse_ci_upper" in summary, "mse_ci_upper missing from fix_summary.json"

    assert isinstance(summary["mse_ci_lower"], (int, float)), "mse_ci_lower must be a number"
    assert isinstance(summary["mse_ci_upper"], (int, float)), "mse_ci_upper must be a number"

def test_mlflow_run_and_metrics():
    summary_path = "/home/user/pipeline/fix_summary.json"
    if not os.path.isfile(summary_path):
        pytest.skip("fix_summary.json not found.")

    with open(summary_path, 'r') as f:
        summary = json.load(f)

    run_id = summary.get("run_id")
    if not run_id:
        pytest.fail("run_id is empty or missing.")

    url = f"http://127.0.0.1:5000/api/2.0/mlflow/runs/get?run_id={run_id}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to MLflow server or run not found: {e}")

    run_data = data.get("run", {}).get("data", {})
    metrics = {m["key"]: m["value"] for m in run_data.get("metrics", [])}

    assert "mse_ci_lower" in metrics, "mse_ci_lower metric not logged to MLflow."
    assert "mse_ci_upper" in metrics, "mse_ci_upper metric not logged to MLflow."

    # Check that the JSON values match the MLflow values
    assert math.isclose(summary["mse_ci_lower"], metrics["mse_ci_lower"], rel_tol=1e-3), \
        "mse_ci_lower in JSON does not match MLflow metric."
    assert math.isclose(summary["mse_ci_upper"], metrics["mse_ci_upper"], rel_tol=1e-3), \
        "mse_ci_upper in JSON does not match MLflow metric."

def test_code_changes():
    train_path = "/home/user/pipeline/train.py"
    assert os.path.isfile(train_path), "train.py is missing."

    with open(train_path, 'r') as f:
        code = f.read()

    # Check for correct train_test_split ordering and fit_transform usage
    assert "train_test_split" in code, "train_test_split is missing."
    assert "fit_transform" in code, "fit_transform is missing."

    # A simple heuristic to ensure train_test_split happens before fit_transform on imputer/scaler
    split_idx = code.find("train_test_split")
    imputer_fit_idx = code.find("fit_transform", split_idx)

    assert imputer_fit_idx > split_idx, \
        "Data leakage not fixed: fit_transform appears to be called before train_test_split."