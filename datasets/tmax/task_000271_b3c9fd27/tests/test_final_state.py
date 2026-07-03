# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_pagerank_csv_exists():
    agent_file = '/home/user/pagerank.csv'
    assert os.path.isfile(agent_file), f"The output file {agent_file} does not exist."

def test_pagerank_csv_format_and_accuracy():
    agent_file = '/home/user/pagerank.csv'
    golden_file = '/app/golden_pagerank.csv'

    assert os.path.isfile(agent_file), f"Missing {agent_file}"
    assert os.path.isfile(golden_file), f"Missing {golden_file}"

    try:
        agent_df = pd.read_csv(agent_file)
    except Exception as e:
        pytest.fail(f"Failed to parse {agent_file} as CSV: {e}")

    golden_df = pd.read_csv(golden_file)

    # Check headers
    expected_columns = ['NodeID', 'PageRank']
    assert list(agent_df.columns) == expected_columns, f"Expected columns {expected_columns}, got {list(agent_df.columns)}"

    # Check sorting
    assert agent_df['NodeID'].is_monotonic_increasing, "The NodeID column is not sorted in ascending order."

    # Check length
    assert len(agent_df) == len(golden_df), f"Expected {len(golden_df)} rows, got {len(agent_df)} rows."

    # Ensure NodeIDs match exactly
    assert np.array_equal(agent_df['NodeID'].values, golden_df['NodeID'].values), "NodeIDs in the output do not match the expected NodeIDs."

    # Compute MSE
    mse = np.mean((agent_df['PageRank'] - golden_df['PageRank'])**2)

    threshold = 1e-6
    assert mse < threshold, f"PageRank MSE is {mse}, which is not strictly less than the threshold {threshold}."