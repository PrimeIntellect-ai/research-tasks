# test_final_state.py
import os
import pandas as pd
import pytest

def test_cracked_jwts_f1_score():
    agent_output_path = '/home/user/cracked_jwts.csv'
    truth_path = '/truth/ground_truth_jwts.csv'

    assert os.path.exists(agent_output_path), f"Agent output file not found at {agent_output_path}"
    assert os.path.exists(truth_path), f"Truth file not found at {truth_path}"

    try:
        truth_df = pd.read_csv(truth_path)
    except Exception as e:
        pytest.fail(f"Failed to read truth CSV: {e}")

    try:
        agent_df = pd.read_csv(agent_output_path)
    except Exception as e:
        pytest.fail(f"Failed to read agent CSV: {e}")

    assert 'id' in agent_df.columns and 'secret' in agent_df.columns, "Agent CSV must contain 'id' and 'secret' columns"

    # Convert rows to tuples for set operations
    truth_set = set(tuple(x) for x in truth_df[['id', 'secret']].values)
    agent_set = set(tuple(x) for x in agent_df[['id', 'secret']].values)

    tp = len(truth_set.intersection(agent_set))
    fp = len(agent_set - truth_set)
    fn = len(truth_set - agent_set)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.99, f"F1-Score {f1:.4f} is below threshold 0.99. Precision: {precision:.4f}, Recall: {recall:.4f}"