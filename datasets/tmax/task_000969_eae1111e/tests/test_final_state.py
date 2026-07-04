# test_final_state.py
import os
import pandas as pd
import pytest

def test_cycles_f1_score():
    agent_file = '/home/user/cycles.csv'
    truth_file = '/app/truth_cycles.csv'

    assert os.path.exists(truth_file), f"Truth file missing at {truth_file}"
    assert os.path.exists(agent_file), f"Agent output file missing at {agent_file}"

    try:
        agent_df = pd.read_csv(agent_file, header=None)
        agent_cycles = set([tuple(x) for x in agent_df.to_numpy()])
    except Exception as e:
        pytest.fail(f"Failed to read agent's cycles.csv: {e}")

    try:
        truth_df = pd.read_csv(truth_file, header=None)
        truth_cycles = set([tuple(x) for x in truth_df.to_numpy()])
    except Exception as e:
        pytest.fail(f"Failed to read truth_cycles.csv: {e}")

    intersection = len(agent_cycles.intersection(truth_cycles))
    precision = intersection / len(agent_cycles) if len(agent_cycles) > 0 else 0
    recall = intersection / len(truth_cycles) if len(truth_cycles) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.99, f"F1 Score {f1:.4f} is below the threshold of 0.99. Precision: {precision:.4f}, Recall: {recall:.4f}"