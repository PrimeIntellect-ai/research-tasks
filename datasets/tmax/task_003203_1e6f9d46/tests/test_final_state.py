# test_final_state.py
import os
import subprocess
import pytest
import pandas as pd
import numpy as np

def test_output_csv_exists():
    assert os.path.isfile("/home/user/output.csv"), "The output file /home/user/output.csv does not exist."

def test_output_mse_against_oracle():
    output_path = "/home/user/output.csv"
    data_path = "/home/user/data.csv"
    truth_path = "/tmp/truth.csv"
    oracle_path = "/app/reference_oracle"

    assert os.path.isfile(output_path), f"{output_path} is missing."
    assert os.path.isfile(data_path), f"{data_path} is missing."
    assert os.path.isfile(oracle_path), f"{oracle_path} is missing."

    # Run the oracle to generate the ground truth
    try:
        subprocess.run([oracle_path, data_path, truth_path], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run the reference oracle: {e.stderr.decode('utf-8')}")

    assert os.path.isfile(truth_path), f"Oracle failed to produce {truth_path}."

    try:
        df_agent = pd.read_csv(output_path).sort_values('id').reset_index(drop=True)
    except Exception as e:
        pytest.fail(f"Failed to read agent's output CSV: {e}")

    try:
        df_truth = pd.read_csv(truth_path).sort_values('id').reset_index(drop=True)
    except Exception as e:
        pytest.fail(f"Failed to read truth CSV: {e}")

    assert len(df_agent) == len(df_truth), f"Row count mismatch: Agent has {len(df_agent)} rows, Truth has {len(df_truth)} rows."

    assert 'value' in df_agent.columns, "The agent's output CSV is missing the 'value' column."
    assert 'value' in df_truth.columns, "The truth CSV is missing the 'value' column."

    # Compute Mean Squared Error
    mse = np.mean((df_agent['value'] - df_truth['value'])**2)
    threshold = 1e-8

    assert mse < threshold, f"MSE is {mse}, which is not strictly less than the threshold {threshold}."