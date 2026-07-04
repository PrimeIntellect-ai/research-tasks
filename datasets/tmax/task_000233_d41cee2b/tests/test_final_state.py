# test_final_state.py

import os
import json
import pytest
import pandas as pd
import numpy as np

def test_parsed_telemetry_exists_and_format():
    """Check that the intermediate parsed CSV exists and has the correct columns."""
    csv_path = "/home/user/parsed_telemetry.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."

    df = pd.read_csv(csv_path)
    expected_columns = {'time', 'sensor', 'value'}
    assert set(df.columns) == expected_columns, f"Columns in {csv_path} must be exactly {expected_columns}, got {set(df.columns)}"

def test_imputed_telemetry_mse():
    """Calculate the MSE of the imputed telemetry CSV and check if it's within tolerance."""
    csv_path = "/home/user/imputed_telemetry.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."

    expected_df = pd.DataFrame({
        'time': [0, 0, 10, 10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60],
        'sensor': ['Alpha', 'Beta'] * 7,
        'value': [12.0, 50.0, 14.5, 48.2, 16.0, 47.0, 17.5, 46.0, 18.0, 45.0, 19.5, 44.5, 20.0, 44.0]
    })

    try:
        agent_df = pd.read_csv(csv_path)
        # Standardize columns to lower case just in case
        agent_df.columns = [c.lower() for c in agent_df.columns]

        merged = pd.merge(expected_df, agent_df, on=['time', 'sensor'], suffixes=('_expected', '_actual'))
        mse = np.mean((merged['value_expected'] - merged['value_actual']) ** 2)
    except Exception as e:
        pytest.fail(f"Failed to process {csv_path} for MSE calculation: {e}")

    assert mse <= 0.1, f"MSE {mse} exceeded threshold 0.1 for imputed values."

def test_summary_json():
    """Check that the summary JSON exists and contains the correct means based on the imputed data."""
    json_path = "/home/user/summary.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "Alpha" in summary, "Key 'Alpha' missing in summary JSON."
    assert "Beta" in summary, "Key 'Beta' missing in summary JSON."
    assert "mean" in summary["Alpha"], "Key 'mean' missing in summary['Alpha']."
    assert "mean" in summary["Beta"], "Key 'mean' missing in summary['Beta']."

    # Calculate expected means from ground truth
    expected_alpha_mean = np.mean([12.0, 14.5, 16.0, 17.5, 18.0, 19.5, 20.0])
    expected_beta_mean = np.mean([50.0, 48.2, 47.0, 46.0, 45.0, 44.5, 44.0])

    agent_alpha_mean = summary["Alpha"]["mean"]
    agent_beta_mean = summary["Beta"]["mean"]

    assert abs(agent_alpha_mean - expected_alpha_mean) <= 0.5, \
        f"Alpha mean {agent_alpha_mean} is too far from expected {expected_alpha_mean}"
    assert abs(agent_beta_mean - expected_beta_mean) <= 0.5, \
        f"Beta mean {agent_beta_mean} is too far from expected {expected_beta_mean}"