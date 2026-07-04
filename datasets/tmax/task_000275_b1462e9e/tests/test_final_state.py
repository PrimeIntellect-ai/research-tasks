# test_final_state.py

import os
import pytest
import pandas as pd
from sklearn.metrics import mean_squared_error

def test_results_csv_exists():
    """Check if the agent generated the results.csv file."""
    path = "/home/user/results.csv"
    assert os.path.exists(path), f"Agent did not create the expected output file: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"

def test_results_mse():
    """Verify the Temporal Impact Scores against the golden reference using MSE."""
    agent_file = "/home/user/results.csv"
    truth_file = "/app/golden_results.csv"

    assert os.path.exists(agent_file), f"Missing agent file: {agent_file}"
    assert os.path.exists(truth_file), f"Missing truth file: {truth_file}"

    try:
        agent_df = pd.read_csv(agent_file)
    except Exception as e:
        pytest.fail(f"Failed to read agent's CSV file: {e}")

    try:
        truth_df = pd.read_csv(truth_file)
    except Exception as e:
        pytest.fail(f"Failed to read golden CSV file: {e}")

    assert 'node_id' in agent_df.columns, "Agent's CSV is missing the 'node_id' column."
    assert 'impact_score' in agent_df.columns, "Agent's CSV is missing the 'impact_score' column."

    agent_df = agent_df.sort_values('node_id').reset_index(drop=True)
    truth_df = truth_df.sort_values('node_id').reset_index(drop=True)

    assert len(agent_df) == len(truth_df), f"Row count mismatch. Expected {len(truth_df)} rows, got {len(agent_df)}."

    # Check if node_ids match exactly
    pd.testing.assert_series_equal(
        agent_df['node_id'], 
        truth_df['node_id'], 
        obj="Node IDs",
        check_dtype=False
    )

    # Calculate MSE
    mse = mean_squared_error(truth_df['impact_score'], agent_df['impact_score'])
    threshold = 0.01

    assert mse <= threshold, f"MSE {mse:.6f} exceeds threshold {threshold}. Agent's scores are not accurate enough."