# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_output_file_exists():
    """Check if the agent generated the output file."""
    output_path = "/home/user/output.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

def test_output_format_and_metric():
    """Check if the output matches the expected format and the MSE is within threshold."""
    output_path = "/home/user/output.csv"
    golden_path = "/opt/verifier/golden_output.csv"

    assert os.path.isfile(golden_path), f"Golden output file {golden_path} is missing. Setup error."

    try:
        agent_df = pd.read_csv(output_path)
    except Exception as e:
        pytest.fail(f"Failed to read {output_path} as CSV: {e}")

    try:
        golden_df = pd.read_csv(golden_path)
    except Exception as e:
        pytest.fail(f"Failed to read {golden_path} as CSV: {e}")

    # Check headers
    expected_cols = ['timestamp', 'sensor_id', 'scaled_rolling_avg']
    for col in expected_cols:
        assert col in agent_df.columns, f"Missing expected column '{col}' in output.csv"

    # Sort and reset index
    agent_df = agent_df.sort_values(['timestamp', 'sensor_id']).reset_index(drop=True)
    golden_df = golden_df.sort_values(['timestamp', 'sensor_id']).reset_index(drop=True)

    # Check lengths
    assert len(agent_df) == len(golden_df), (
        f"Row count mismatch: expected {len(golden_df)} rows, but got {len(agent_df)} rows."
    )

    # Compute MSE
    agent_vals = pd.to_numeric(agent_df['scaled_rolling_avg'], errors='coerce').fillna(0.0)
    golden_vals = pd.to_numeric(golden_df['scaled_rolling_avg'], errors='coerce').fillna(0.0)

    mse = np.mean((agent_vals - golden_vals) ** 2)
    threshold = 0.05

    assert mse <= threshold, (
        f"MSE {mse:.4f} exceeds threshold of {threshold}. "
        "The computed scaled rolling averages differ too much from the expected values."
    )