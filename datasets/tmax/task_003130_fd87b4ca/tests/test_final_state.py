# test_final_state.py

import os
import subprocess
import numpy as np
import pandas as pd
import pytest

def test_posterior_means_mse():
    results_path = "/home/user/pipeline/results/posterior_means.csv"
    assert os.path.exists(results_path), f"Missing results file: {results_path}"

    with open(results_path, "r") as f:
        content = f.read().strip().split(",")

    assert len(content) == 3, f"Expected exactly 3 comma-separated values in {results_path}, got {len(content)}"

    try:
        k1_est, k2_est, k3_est = map(float, content)
    except ValueError:
        pytest.fail(f"Could not parse parameters as floats from {results_path}. Content: {content}")

    # Run blackbox_reactor for true parameters
    true_cmd = ["/app/blackbox_reactor", "0.04", "10000", "30000000"]
    true_res = subprocess.run(true_cmd, capture_output=True, text=True)
    assert true_res.returncode == 0, f"Failed to run blackbox_reactor for true parameters. Error: {true_res.stderr}"

    # Run blackbox_reactor for estimated parameters
    est_cmd = ["/app/blackbox_reactor", str(k1_est), str(k2_est), str(k3_est)]
    est_res = subprocess.run(est_cmd, capture_output=True, text=True)
    assert est_res.returncode == 0, f"Failed to run blackbox_reactor for estimated parameters. Error: {est_res.stderr}"

    def parse_trajectory(output):
        lines = output.strip().split("\n")
        data = []
        for line in lines:
            if line.strip():
                data.append([float(x) for x in line.strip().split()])
        return np.array(data)

    true_traj = parse_trajectory(true_res.stdout)
    est_traj = parse_trajectory(est_res.stdout)

    assert true_traj.shape == est_traj.shape, f"Trajectory shape mismatch: true {true_traj.shape}, est {est_traj.shape}. Check if blackbox_reactor output format changed."

    mse = np.mean((true_traj - est_traj) ** 2)
    threshold = 1e-4

    assert mse <= threshold, f"Trajectory MSE {mse:.6e} exceeds threshold {threshold:.6e}. Estimated parameters: k1={k1_est}, k2={k2_est}, k3={k3_est}"

def test_clean_experiment_data():
    clean_path = "/home/user/pipeline/data/clean_experiment.csv"
    assert os.path.exists(clean_path), f"Missing clean data file: {clean_path}"

    try:
        df = pd.read_csv(clean_path)
    except Exception as e:
        pytest.fail(f"Failed to read {clean_path} as CSV: {e}")

    expected_cols = ["time", "A", "B", "C"]
    assert list(df.columns) == expected_cols, f"Unexpected columns in clean data. Expected {expected_cols}, got {list(df.columns)}"
    assert len(df) == 100, f"Expected exactly 100 rows in clean data, got {len(df)}"