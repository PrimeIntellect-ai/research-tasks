# test_final_state.py

import os
import pytest
import pandas as pd
import numpy as np

def test_traffic_report_mae():
    agent_csv = "/home/user/traffic_report.csv"
    reference_csv = "/app/reference_report.csv"

    assert os.path.isfile(agent_csv), f"Agent output CSV is missing: {agent_csv}"
    assert os.path.isfile(reference_csv), f"Reference CSV is missing: {reference_csv}"

    try:
        df_agent = pd.read_csv(agent_csv)
    except Exception as e:
        pytest.fail(f"Failed to read agent CSV: {e}")

    try:
        df_ref = pd.read_csv(reference_csv)
    except Exception as e:
        pytest.fail(f"Failed to read reference CSV: {e}")

    assert 'window_id' in df_agent.columns, "Agent CSV missing 'window_id' column"
    assert 'p_congested' in df_agent.columns, "Agent CSV missing 'p_congested' column"

    # Align by window_id
    try:
        df_agent = df_agent.set_index('window_id')
        df_ref = df_ref.set_index('window_id')
    except Exception as e:
        pytest.fail(f"Failed to set index to 'window_id': {e}")

    # Find common indices to compare
    common_indices = df_agent.index.intersection(df_ref.index)
    assert len(common_indices) > 0, "No common window_ids found between agent and reference CSVs"

    # Check if all reference windows are present
    missing_windows = df_ref.index.difference(df_agent.index)
    assert len(missing_windows) == 0, f"Agent CSV is missing window_ids: {list(missing_windows)}"

    # Calculate MAE
    mae = np.mean(np.abs(df_agent.loc[common_indices, 'p_congested'] - df_ref.loc[common_indices, 'p_congested']))

    threshold = 0.01
    assert mae <= threshold, f"MAE of p_congested is {mae:.5f}, which exceeds the maximum acceptable threshold of {threshold}"