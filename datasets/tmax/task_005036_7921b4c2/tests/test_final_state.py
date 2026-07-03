# test_final_state.py

import os
import pytest
import pandas as pd
import numpy as np

def test_hourly_errors_csv_exists():
    """Check that the agent generated the output file at the correct path."""
    path = "/home/user/hourly_errors.csv"
    assert os.path.isfile(path), f"Agent did not create the required output file at {path}"

def test_hourly_errors_mse():
    """
    Calculate the Mean Squared Error (MSE) between the agent's output
    and the ground truth, and assert that it meets the threshold.
    """
    agent_file = "/home/user/hourly_errors.csv"
    truth_file = "/tmp/ground_truth.csv"

    assert os.path.isfile(agent_file), "Agent output file is missing."
    assert os.path.isfile(truth_file), "Ground truth file is missing."

    try:
        df_agent = pd.read_csv(agent_file)
    except Exception as e:
        pytest.fail(f"Failed to read agent's CSV file: {e}")

    try:
        df_truth = pd.read_csv(truth_file)
    except Exception as e:
        pytest.fail(f"Failed to read ground truth CSV file: {e}")

    # Check if required columns exist
    assert 'Hour' in df_agent.columns, "Agent output is missing the 'Hour' column."
    assert 'ErrorCount' in df_agent.columns, "Agent output is missing the 'ErrorCount' column."

    # Merge on Hour to align rows
    merged = pd.merge(df_truth, df_agent, on='Hour', how='left', suffixes=('_truth', '_agent'))
    merged['ErrorCount_agent'] = merged['ErrorCount_agent'].fillna(0)

    # Compute MSE
    mse = np.mean((merged['ErrorCount_truth'] - merged['ErrorCount_agent']) ** 2)

    # Threshold check
    threshold = 0.0
    assert mse <= threshold, f"MSE of ErrorCount is {mse}, which is greater than the threshold {threshold}. The aggregation is incorrect."