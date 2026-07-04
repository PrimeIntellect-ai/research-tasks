# test_final_state.py

import os
import json
import pytest

def test_pagerank_mae():
    """Test that the agent's PageRank scores meet the MAE threshold."""
    truth_path = "/app/ground_truth.json"
    agent_path = "/home/user/pagerank.json"

    assert os.path.exists(truth_path), f"Truth file missing: {truth_path}"
    assert os.path.exists(agent_path), f"Agent output missing: {agent_path}"

    with open(truth_path, "r") as f:
        truth = json.load(f)

    with open(agent_path, "r") as f:
        agent = json.load(f)

    assert truth, "Ground truth JSON is empty."

    error_sum = 0.0
    all_keys = set(truth.keys()).union(set(agent.keys()))

    for k in all_keys:
        t_val = truth.get(k, 0.0)
        a_val = agent.get(k, 0.0)
        error_sum += abs(t_val - a_val)

    mae = error_sum / len(all_keys)
    threshold = 0.0001

    assert mae <= threshold, f"MAE {mae} exceeds threshold {threshold}"