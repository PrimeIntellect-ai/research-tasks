# test_final_state.py
import os
import pandas as pd
import numpy as np
import pytest

def test_clean_weather_parquet_mse():
    agent_path = '/app/clean_weather.parquet'
    ref_path = '/truth/reference.parquet'

    assert os.path.exists(agent_path), f"Agent output file not found: {agent_path}"
    assert os.path.exists(ref_path), f"Reference file not found: {ref_path}"

    try:
        agent_df = pd.read_parquet(agent_path)
    except Exception as e:
        pytest.fail(f"Failed to read agent parquet file: {e}")

    try:
        ref_df = pd.read_parquet(ref_path)
    except Exception as e:
        pytest.fail(f"Failed to read reference parquet file: {e}")

    # Check if expected columns are present
    expected_cols = ['Date', 'City', 'Temperature']
    for col in expected_cols:
        assert col in agent_df.columns, f"Missing column '{col}' in agent output. Found columns: {agent_df.columns.tolist()}"

    # Standardize types for comparison
    agent_df['Date'] = pd.to_datetime(agent_df['Date'])
    ref_df['Date'] = pd.to_datetime(ref_df['Date'])

    # Sort and reset index
    agent_df = agent_df.sort_values(['Date', 'City']).reset_index(drop=True)
    ref_df = ref_df.sort_values(['Date', 'City']).reset_index(drop=True)

    # Check shape
    assert len(agent_df) == len(ref_df), f"Expected {len(ref_df)} rows, but got {len(agent_df)} rows."

    # Check Date and City match exactly
    pd.testing.assert_series_equal(
        agent_df['Date'], 
        ref_df['Date'], 
        check_names=False, 
        obj='Date column'
    )
    pd.testing.assert_series_equal(
        agent_df['City'].astype(str), 
        ref_df['City'].astype(str), 
        check_names=False, 
        obj='City column'
    )

    # Calculate MSE
    mse = np.mean((agent_df['Temperature'] - ref_df['Temperature'])**2)

    assert mse <= 0.1, f"MSE is {mse:.4f}, which is greater than the threshold of 0.1."