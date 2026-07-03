# test_final_state.py
import os
import pandas as pd
import numpy as np
import pytest

def test_executable_exists():
    executable_path = "/home/user/aggregator"
    assert os.path.isfile(executable_path), f"Executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_throughput_stats_csv():
    agent_file = "/home/user/throughput_stats.csv"
    ref_file = "/tmp/reference_stats.csv"

    assert os.path.isfile(agent_file), f"Output file not found at {agent_file}"
    assert os.path.isfile(ref_file), f"Reference file not found at {ref_file}"

    try:
        df_agent = pd.read_csv(agent_file)
    except Exception as e:
        pytest.fail(f"Failed to read agent's CSV file: {e}")

    try:
        df_ref = pd.read_csv(ref_file)
    except Exception as e:
        pytest.fail(f"Failed to read reference CSV file: {e}")

    required_columns = ['bucket_ts', 'lang', 'hourly_words', 'rolling_3h_avg']
    for col in required_columns:
        assert col in df_agent.columns, f"Agent's CSV is missing required column: {col}"

    # Merge on bucket_ts and lang
    merged = pd.merge(df_ref, df_agent, on=['bucket_ts', 'lang'], suffixes=('_ref', '_agent'), how='left')
    merged['rolling_3h_avg_agent'] = merged['rolling_3h_avg_agent'].fillna(0.0)

    max_ae = np.max(np.abs(merged['rolling_3h_avg_ref'] - merged['rolling_3h_avg_agent']))

    assert max_ae <= 0.05, f"Max Absolute Error (MaxAE) of rolling_3h_avg is {max_ae}, which exceeds the threshold of 0.05."

def test_sorting_of_output():
    agent_file = "/home/user/throughput_stats.csv"
    if not os.path.isfile(agent_file):
        pytest.skip("Output file not found, skipping sorting test.")

    df_agent = pd.read_csv(agent_file)
    if 'bucket_ts' not in df_agent.columns or 'lang' not in df_agent.columns:
        pytest.skip("Missing columns, skipping sorting test.")

    # Check if the dataframe is sorted by bucket_ts (ascending), then lang (alphabetically)
    is_sorted = df_agent.equals(df_agent.sort_values(by=['bucket_ts', 'lang']).reset_index(drop=True))
    assert is_sorted, "The output file is not correctly sorted by 'bucket_ts' ascending, then 'lang' alphabetically."