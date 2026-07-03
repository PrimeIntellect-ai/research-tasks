# test_final_state.py
import gzip
import os
import pytest
import pandas as pd

def test_final_events_f1_score():
    agent_file = '/home/user/final_events.csv.gz'
    truth_file = '/app/.hidden_truth.csv'

    assert os.path.exists(agent_file), f"Agent output file {agent_file} does not exist."
    assert os.path.exists(truth_file), f"Truth file {truth_file} does not exist."

    try:
        truth_df = pd.read_csv(truth_file, names=['Timestamp', 'Code', 'FrameSize'])
    except Exception as e:
        pytest.fail(f"Failed to read truth file: {e}")

    try:
        with gzip.open(agent_file, 'rt') as f:
            agent_df = pd.read_csv(f, names=['Timestamp', 'Code', 'FrameSize'])
    except Exception as e:
        pytest.fail(f"Failed to read or parse agent output {agent_file}. Ensure it is a valid gzip compressed CSV file. Error: {e}")

    merged = pd.merge(truth_df, agent_df, how='inner')

    correct_count = len(merged)
    precision = correct_count / len(agent_df) if len(agent_df) > 0 else 0
    recall = correct_count / len(truth_df) if len(truth_df) > 0 else 0

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"F1 Score {f1:.4f} is less than the required threshold of 0.95. Precision: {precision:.4f}, Recall: {recall:.4f}"