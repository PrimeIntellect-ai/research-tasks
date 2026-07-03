# test_final_state.py
import os
import json
import pandas as pd
import numpy as np

def test_experiment_log_exists():
    """Check if the experiment log file exists."""
    log_path = "/home/user/data_gen/experiment_log.json"
    assert os.path.exists(log_path), f"Experiment log missing at {log_path}"
    assert os.path.isfile(log_path), f"Path {log_path} is not a file"

    # Try parsing it as JSON to ensure it's valid
    try:
        with open(log_path, 'r') as f:
            json.load(f)
    except json.JSONDecodeError:
        assert False, f"File {log_path} is not valid JSON"

def test_synthetic_data_statistics():
    """Validate the generated synthetic dataset against the target statistics."""
    csv_path = "/home/user/data_gen/synthetic_data.csv"
    assert os.path.exists(csv_path), f"Synthetic data CSV missing at {csv_path}"

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        assert False, f"Failed to read CSV at {csv_path}: {e}"

    assert len(df) == 50000, f"Expected 50000 rows in synthetic data, got {len(df)}"

    expected_cols = ['f1', 'f2', 'f3']
    for col in expected_cols:
        assert col in df.columns, f"Expected column '{col}' missing from CSV headers"

    # Ground truth parameters
    true_mean = np.array([1.50, -2.00, 3.50])
    true_cov = np.array([
        [2.00, 0.40, -0.30],
        [0.40, 1.50, 0.20],
        [-0.30, 0.20, 3.00]
    ])

    emp_mean = df[['f1', 'f2', 'f3']].mean().values
    emp_cov = df[['f1', 'f2', 'f3']].cov().values

    mean_err = np.max(np.abs(emp_mean - true_mean))
    cov_err = np.max(np.abs(emp_cov - true_cov))

    total_err = mean_err + cov_err
    threshold = 0.05

    assert total_err <= threshold, (
        f"Total error (max mean err + max cov err) is {total_err:.5f}, "
        f"which exceeds the threshold of {threshold}. "
        f"Mean err: {mean_err:.5f}, Cov err: {cov_err:.5f}"
    )