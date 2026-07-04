# test_final_state.py

import os
import subprocess
import pytest

def test_venv_exists():
    """Check if the Python virtual environment was created."""
    assert os.path.exists("/home/user/venv/bin/python"), "Virtual environment python binary not found at /home/user/venv/bin/python"

def test_run_experiment_script_exists():
    """Check if the experiment script was created."""
    assert os.path.exists("/home/user/run_experiment.py"), "The script /home/user/run_experiment.py does not exist."

def test_mlflow_tracking_and_metrics():
    """
    Verify the MLflow experiment 'PCA_Benchmarking' and its runs.
    Uses the student's virtual environment to import mlflow and numpy.
    """
    verification_script = """
import os
import sys

try:
    import mlflow
    import numpy as np
except ImportError as e:
    print(f"IMPORT_ERROR: {e}")
    sys.exit(0)

mlflow.set_tracking_uri("file:///home/user/mlruns")
experiment = mlflow.get_experiment_by_name("PCA_Benchmarking")

if experiment is None:
    print("NO_EXPERIMENT: Experiment 'PCA_Benchmarking' not found.")
    sys.exit(0)

runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])

if len(runs) != 3:
    print(f"WRONG_RUNS_COUNT: Expected 3 runs, found {len(runs)}")
    sys.exit(0)

expected_ks = {"2", "5", "10"}
actual_ks = set(runs["params.k"].dropna().astype(str).tolist())

if expected_ks != actual_ks:
    print(f"WRONG_KS: Expected runs for k in {expected_ks}, but got {actual_ks}")
    sys.exit(0)

for _, run in runs.iterrows():
    k = int(run["params.k"])
    mse = run["metrics.mse"]
    avg_time = run["metrics.avg_inference_time_sec"]

    if np.isnan(mse) or np.isnan(avg_time):
        print(f"MISSING_METRICS: Missing metrics for run with k={k}")
        sys.exit(0)

    artifact_uri = run["artifact_uri"].replace("file://", "")
    artifact_path = os.path.join(artifact_uri, "projection_matrix.npy")

    if not os.path.exists(artifact_path):
        print(f"MISSING_ARTIFACT: Artifact projection_matrix.npy not found for run k={k} at {artifact_path}")
        sys.exit(0)

    matrix = np.load(artifact_path)
    if matrix.shape != (20, k):
        print(f"WRONG_SHAPE: Expected projection matrix shape (20, {k}), got {matrix.shape}")
        sys.exit(0)

print("SUCCESS")
"""
    script_path = "/tmp/verify_mlflow_runs.py"
    with open(script_path, "w") as f:
        f.write(verification_script)

    result = subprocess.run(
        ["/home/user/venv/bin/python", script_path],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()
    assert output == "SUCCESS", f"MLflow verification failed. Reason: {output}\nStderr: {result.stderr}"