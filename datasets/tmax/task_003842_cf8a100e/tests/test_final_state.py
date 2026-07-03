# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_pagerank_mse():
    agent_output_path = '/home/user/pagerank_output.csv'
    truth_output_path = '/tmp/ground_truth_pagerank.csv'

    assert os.path.isfile(agent_output_path), f"Agent output file not found at {agent_output_path}"
    assert os.path.isfile(truth_output_path), f"Ground truth file not found at {truth_output_path}"

    # Load agent output
    try:
        agent_df = pd.read_csv(agent_output_path, header=None, names=['node', 'pr'])
    except Exception as e:
        pytest.fail(f"Failed to read agent output CSV: {e}")

    agent_df = agent_df.sort_values('node').reset_index(drop=True)

    # Load ground truth
    try:
        truth_df = pd.read_csv(truth_output_path, header=None, names=['node', 'pr'])
    except Exception as e:
        pytest.fail(f"Failed to read ground truth CSV: {e}")

    truth_df = truth_df.sort_values('node').reset_index(drop=True)

    assert len(agent_df) == len(truth_df), (
        f"Number of nodes in output ({len(agent_df)}) does not match "
        f"ground truth ({len(truth_df)})."
    )

    # Verify node IDs match exactly
    if not (agent_df['node'] == truth_df['node']).all():
        pytest.fail("Node IDs in the output do not match the expected node IDs.")

    # Calculate MSE
    mse = np.mean((agent_df['pr'] - truth_df['pr'])**2)

    assert mse <= 1e-12, f"MSE {mse} is above the threshold of 1e-12"