# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_final_sample_mae():
    agent_file = '/home/user/final_sample.csv'
    events_file = '/home/user/events.csv'

    assert os.path.exists(agent_file), f"Output file {agent_file} does not exist. The pipeline script may not have run or failed to produce output."
    assert os.path.exists(events_file), f"Input file {events_file} is missing."

    try:
        df_agent = pd.read_csv(agent_file)
    except Exception as e:
        pytest.fail(f"Could not read {agent_file} as CSV: {e}")

    # Re-derive reference logic from the original events.csv
    df_ref = pd.read_csv(events_file)

    # The feature extractor multiplies raw_value by 1.5
    df_ref['extracted_value'] = df_ref['raw_value'] * 1.5
    df_ref = df_ref.drop(columns=['raw_value'])

    # Sort chronologically
    df_ref = df_ref.sort_values('timestamp').reset_index(drop=True)

    # Calculate rolling average (window=3)
    df_ref['rolling_avg'] = df_ref['extracted_value'].rolling(window=3, min_periods=1).mean()

    # Stratified sampling: first 2 chronologically per category
    df_ref = df_ref.groupby('category').head(2).reset_index(drop=True)

    # Check required columns in agent output
    required_columns = ['id', 'timestamp', 'category', 'extracted_value', 'rolling_avg']
    for col in required_columns:
        assert col in df_agent.columns, f"Column '{col}' is missing from {agent_file}"

    # Merge and calculate MAE
    merged = pd.merge(df_ref, df_agent, on=['id', 'timestamp', 'category'], suffixes=('_ref', '_agent'))

    if len(merged) != len(df_ref):
        pytest.fail(f"Expected {len(df_ref)} rows in final sample matching reference IDs/timestamps/categories, but found {len(merged)} valid matching rows. Deduplication or stratified sampling logic is likely incorrect.")

    mae = np.mean(np.abs(merged['rolling_avg_ref'] - merged['rolling_avg_agent']))

    threshold = 0.05
    assert mae <= threshold, f"MAE {mae:.4f} exceeds threshold {threshold}. The rolling average calculation is incorrect."