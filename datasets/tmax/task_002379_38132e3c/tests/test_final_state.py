# test_final_state.py
import os
import pandas as pd
import numpy as np
import pytest

def test_node_stats_mae():
    truth_path = "/tmp/truth_node_stats.csv"
    agent_path = "/home/user/node_stats.csv"

    assert os.path.exists(truth_path), f"Truth file {truth_path} missing. This is an environment error."
    assert os.path.exists(agent_path), f"Agent output file {agent_path} missing."

    try:
        truth = pd.read_csv(truth_path)
        agent = pd.read_csv(agent_path)
    except Exception as e:
        pytest.fail(f"Failed to read CSV files: {e}")

    assert len(agent) == 10, f"Expected exactly 10 rows in {agent_path}, got {len(agent)}"

    expected_cols = ["node", "total_out_weight", "total_in_weight"]
    for col in expected_cols:
        assert col in agent.columns, f"Missing column '{col}' in {agent_path}"

    mae_out = np.abs(truth['total_out_weight'] - agent['total_out_weight']).mean()
    mae_in = np.abs(truth['total_in_weight'] - agent['total_in_weight']).mean()

    mae_total = (mae_out + mae_in) / 2.0

    assert mae_total <= 0.0, f"MAE is {mae_total}, expected <= 0.0. Output stats do not perfectly match the video frames."

def test_cpp_file_exists():
    cpp_path = "/home/user/aggregate.cpp"
    assert os.path.exists(cpp_path), f"C++ source file {cpp_path} missing. You must write the aggregation logic in C++."