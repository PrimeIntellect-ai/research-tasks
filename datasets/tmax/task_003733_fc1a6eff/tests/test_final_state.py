# test_final_state.py

import os
import pandas as pd
import numpy as np
import pytest

def test_influence_scores_mse():
    agent_file = '/home/user/influence_scores.csv'
    ref_file = '/app/ground_truth_scores.csv'

    assert os.path.isfile(agent_file), f"Agent's output file {agent_file} is missing."
    assert os.path.isfile(ref_file), f"Ground truth file {ref_file} is missing."

    try:
        agent_df = pd.read_csv(agent_file)
    except Exception as e:
        pytest.fail(f"Failed to read agent's output file as CSV: {e}")

    try:
        ref_df = pd.read_csv(ref_file)
    except Exception as e:
        pytest.fail(f"Failed to read ground truth file as CSV: {e}")

    assert 'node' in agent_df.columns, "Agent's output must contain a 'node' column."
    assert 'score' in agent_df.columns, "Agent's output must contain a 'score' column."

    # Ensure node types match (convert to string to be safe)
    agent_df['node'] = agent_df['node'].astype(str)
    ref_df['node'] = ref_df['node'].astype(str)

    # Merge and calculate MSE
    merged = pd.merge(ref_df, agent_df, on='node', suffixes=('_ref', '_agent'))

    assert len(merged) == len(ref_df), f"Agent's output is missing nodes. Expected {len(ref_df)}, found {len(merged)} matching nodes."

    mse = np.mean((merged['score_ref'] - merged['score_agent'])**2)

    threshold = 0.001
    assert mse <= threshold, f"MSE is too high. Expected <= {threshold}, but got {mse:.6f}."