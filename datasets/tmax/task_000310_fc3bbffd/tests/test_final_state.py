# test_final_state.py

import os
import pandas as pd
import pytest

def test_c_source_exists():
    """Ensure the C source code file exists."""
    assert os.path.isfile('/home/user/tracker.c'), "C source code /home/user/tracker.c is missing."

def test_output_csv_exists():
    """Ensure the output CSV file exists."""
    assert os.path.isfile('/home/user/hourly_summary.csv'), "Output CSV /home/user/hourly_summary.csv is missing."

def test_output_csv_accuracy():
    """Check if the output CSV matches the reference with MAE < 0.2."""
    agent_file = '/home/user/hourly_summary.csv'
    ref_file = '/home/user/reference.csv'

    assert os.path.isfile(agent_file), "Agent output file is missing."
    assert os.path.isfile(ref_file), "Reference file is missing."

    try:
        df_agent = pd.read_csv(agent_file)
    except Exception as e:
        pytest.fail(f"Failed to read agent output CSV: {e}")

    try:
        df_ref = pd.read_csv(ref_file)
    except Exception as e:
        pytest.fail(f"Failed to read reference CSV: {e}")

    assert df_agent.shape == df_ref.shape, f"Shape mismatch: agent {df_agent.shape} vs ref {df_ref.shape}"
    assert list(df_agent.columns) == list(df_ref.columns), f"Column mismatch: agent {list(df_agent.columns)} vs ref {list(df_ref.columns)}"

    # Check numeric columns only to avoid issues with string headers if any exist
    df_agent_numeric = df_agent.apply(pd.to_numeric, errors='coerce')
    df_ref_numeric = df_ref.apply(pd.to_numeric, errors='coerce')

    mae = (df_agent_numeric - df_ref_numeric).abs().max().max()

    assert mae < 0.2, f"Maximum Absolute Error (MAE) is {mae}, which is >= 0.2 threshold."