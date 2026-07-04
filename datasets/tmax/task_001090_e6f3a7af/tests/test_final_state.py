# test_final_state.py

import os
import pytest
import pandas as pd

def test_imputed_csv_exists():
    imputed_path = "/home/user/imputed.csv"
    assert os.path.exists(imputed_path), f"Missing generated dataset at {imputed_path}"
    assert os.path.isfile(imputed_path), f"{imputed_path} is not a file"
    assert os.path.getsize(imputed_path) > 0, f"{imputed_path} is empty"

def test_c_source_exists():
    c_path = "/home/user/calc_metric.c"
    assert os.path.exists(c_path), f"Missing C source file at {c_path}"
    assert os.path.isfile(c_path), f"{c_path} is not a file"

def test_metric_txt_exists_and_valid():
    metric_path = "/home/user/metric.txt"
    assert os.path.exists(metric_path), f"Missing metric output file at {metric_path}"
    assert os.path.isfile(metric_path), f"{metric_path} is not a file"

    with open(metric_path, "r") as f:
        content = f.read().strip()

    try:
        float(content)
    except ValueError:
        pytest.fail(f"Content of {metric_path} is not a valid float: '{content}'")

def test_metric_accuracy():
    imputed_path = "/home/user/imputed.csv"
    metric_path = "/home/user/metric.txt"

    # Ensure dependencies exist before calculating
    assert os.path.exists(imputed_path), f"Cannot verify metric without {imputed_path}"
    assert os.path.exists(metric_path), f"Cannot verify metric without {metric_path}"

    # Compute the expected standard deviation
    df = pd.read_csv(imputed_path)
    assert 'value' in df.columns, f"Column 'value' not found in {imputed_path}"

    valid_rows = df[(df['value'] >= 0.0) & (df['value'] <= 1000.0)]
    expected_std = valid_rows['value'].std(ddof=1)

    # Read the agent's computed metric
    with open(metric_path, 'r') as f:
        agent_val = float(f.read().strip())

    # Calculate absolute error
    error = abs(expected_std - agent_val)
    threshold = 0.005

    assert error <= threshold, (
        f"Metric threshold exceeded! Absolute error is {error:.6f} (Threshold <= {threshold}). "
        f"Expected {expected_std:.6f}, got {agent_val:.6f}."
    )