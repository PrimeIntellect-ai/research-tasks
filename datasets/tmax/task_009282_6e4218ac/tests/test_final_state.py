# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

MLFLOW_URL = "http://127.0.0.1:5000"

def test_mlflow_server_running():
    """Test that the MLflow server is running and responding on port 5000."""
    try:
        req = urllib.request.Request(f"{MLFLOW_URL}/api/2.0/mlflow/experiments/list", method="GET")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, "MLflow server is not returning a 200 status code."
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to MLflow server at {MLFLOW_URL}. Is it running? Error: {e}")

def test_mlflow_runs_logged():
    """Test that the experiment exists and has the correct runs logged."""
    # Get experiment by name
    url = f"{MLFLOW_URL}/api/2.0/mlflow/experiments/get-by-name?experiment_name=Server_Failure_Predictor"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            experiment = data.get("experiment", {})
            experiment_id = experiment.get("experiment_id")
            assert experiment_id is not None, "Experiment 'Server_Failure_Predictor' not found."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to fetch experiment: {e}")

    # Search runs
    search_url = f"{MLFLOW_URL}/api/2.0/mlflow/runs/search"
    payload = json.dumps({"experiment_ids": [experiment_id]}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    try:
        req = urllib.request.Request(search_url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            runs = data.get("runs", [])
            assert len(runs) >= 3, f"Expected at least 3 runs, found {len(runs)}."

            pipelines_found = set()
            for run in runs:
                data_dict = run.get("data", {})
                params = {p["key"]: p["value"] for p in data_dict.get("params", [])}
                metrics = {m["key"]: m["value"] for m in data_dict.get("metrics", [])}

                if "pipeline_name" in params:
                    pipelines_found.add(params["pipeline_name"])

                assert "accuracy" in metrics, f"Run {run['info']['run_id']} is missing the 'accuracy' metric."

            expected_pipelines = {"baseline", "interactions", "log_transform"}
            assert expected_pipelines.issubset(pipelines_found), f"Missing pipelines in MLflow runs. Expected {expected_pipelines}, found {pipelines_found}."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to search runs: {e}")

def test_best_run_json():
    """Test that best_run.json exists and correctly identifies the best run."""
    json_path = "/home/user/best_run.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            best_run_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "best_run_id" in best_run_data, "Missing 'best_run_id' in JSON."
    assert "best_pipeline" in best_run_data, "Missing 'best_pipeline' in JSON."

    # Fetch all runs to find the actual best run
    url = f"{MLFLOW_URL}/api/2.0/mlflow/experiments/get-by-name?experiment_name=Server_Failure_Predictor"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as response:
        exp_data = json.loads(response.read().decode("utf-8"))
        experiment_id = exp_data["experiment"]["experiment_id"]

    search_url = f"{MLFLOW_URL}/api/2.0/mlflow/runs/search"
    payload = json.dumps({"experiment_ids": [experiment_id]}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(search_url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        runs_data = json.loads(response.read().decode("utf-8"))
        runs = runs_data.get("runs", [])

    best_run = None
    best_accuracy = -1.0

    for run in runs:
        data_dict = run.get("data", {})
        metrics = {m["key"]: m["value"] for m in data_dict.get("metrics", [])}
        params = {p["key"]: p["value"] for p in data_dict.get("params", [])}

        accuracy = metrics.get("accuracy", -1.0)
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_run = run

    assert best_run is not None, "No runs with accuracy found."

    expected_best_run_id = best_run["info"]["run_id"]
    expected_best_pipeline = None
    for p in best_run.get("data", {}).get("params", []):
        if p["key"] == "pipeline_name":
            expected_best_pipeline = p["value"]

    assert best_run_data["best_run_id"] == expected_best_run_id, f"Incorrect best_run_id in JSON. Expected {expected_best_run_id}, got {best_run_data['best_run_id']}."
    assert best_run_data["best_pipeline"] == expected_best_pipeline, f"Incorrect best_pipeline in JSON. Expected {expected_best_pipeline}, got {best_run_data['best_pipeline']}."