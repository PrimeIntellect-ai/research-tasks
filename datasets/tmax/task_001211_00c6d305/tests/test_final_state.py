# test_final_state.py

import os
import numpy as np

def test_test_features_mse():
    agent_file = '/home/user/test_features.bin'
    truth_file = '/app/ground_truth_test.bin'

    assert os.path.exists(agent_file), f"Agent output file {agent_file} is missing."
    assert os.path.exists(truth_file), f"Ground truth file {truth_file} is missing."

    agent_data = np.fromfile(agent_file, dtype=np.float64)
    truth_data = np.fromfile(truth_file, dtype=np.float64)

    assert len(agent_data) == len(truth_data), (
        f"Length mismatch: agent produced {len(agent_data)} samples, "
        f"expected {len(truth_data)} samples."
    )

    mse = np.mean((agent_data - truth_data)**2)
    assert mse <= 1e-5, f"MSE {mse} is greater than the threshold 1e-5."

def test_test_stats_file():
    stats_file = '/home/user/test_stats.txt'
    truth_file = '/app/ground_truth_test.bin'

    assert os.path.exists(stats_file), f"Stats file {stats_file} is missing."

    truth_data = np.fromfile(truth_file, dtype=np.float64)
    expected_mean = np.mean(truth_data)
    expected_std = np.std(truth_data, ddof=1)
    n = len(truth_data)
    margin = 1.96 * expected_std / np.sqrt(n)
    expected_lower = expected_mean - margin
    expected_upper = expected_mean + margin

    with open(stats_file, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 3, f"Expected 3 comma-separated values in {stats_file}, got {len(parts)}."

    try:
        agent_mean = float(parts[0])
        agent_lower = float(parts[1])
        agent_upper = float(parts[2])
    except ValueError:
        assert False, f"Could not parse floats from {stats_file}: {content}"

    # Allow a small tolerance for the stats due to potential ddof=0 vs ddof=1 in std dev calculation
    assert abs(agent_mean - expected_mean) < 1e-2, f"Expected mean ~{expected_mean}, got {agent_mean}"
    assert abs(agent_lower - expected_lower) < 1e-2, f"Expected lower bound ~{expected_lower}, got {agent_lower}"
    assert abs(agent_upper - expected_upper) < 1e-2, f"Expected upper bound ~{expected_upper}, got {agent_upper}"