# test_final_state.py

import os
import subprocess
import numpy as np
import pytest

def test_predictions_mse():
    predictions_path = '/home/user/predictions.csv'
    eval_data_path = '/home/user/eval_data.csv'
    oracle_path = '/app/oracle_engine'

    assert os.path.exists(predictions_path), f"Agent output file {predictions_path} does not exist. Did you save the predictions?"
    assert os.path.exists(eval_data_path), f"Evaluation data {eval_data_path} is missing."
    assert os.path.exists(oracle_path), f"Oracle engine {oracle_path} is missing."

    # 1. Run Oracle to get ground truth
    try:
        oracle_out = subprocess.check_output([oracle_path, eval_data_path]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run oracle engine: {e}")

    try:
        expected = np.array([float(x) for x in oracle_out.strip().split('\n') if x.strip()])
    except ValueError:
        pytest.fail("Failed to parse oracle output as floats.")

    # 2. Read Agent's output
    try:
        with open(predictions_path, 'r') as f:
            predicted = np.array([float(x) for x in f.read().strip().split('\n') if x.strip()])
    except ValueError:
        pytest.fail(f"Failed to parse {predictions_path} as floats. Ensure it contains one float per line.")

    # Ensure the lengths match before calculating MSE
    assert len(expected) == len(predicted), f"Length mismatch: expected {len(expected)} predictions, got {len(predicted)}."

    # 3. Calculate Metric
    mse = np.mean((expected - predicted)**2)

    # 4. Assert Threshold
    assert mse < 1e-10, f"Output MSE {mse} is above threshold 1e-10. Convergence/precision issue not fully fixed."