# test_final_state.py

import os
import numpy as np
import pytest

def test_model_weights_accuracy():
    output_path = "/home/user/model_weights.txt"

    assert os.path.isfile(output_path), f"Output file not found at {output_path}"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content, f"Output file {output_path} is empty"

    try:
        agent_weights = np.array([float(x.strip()) for x in content.split(',')])
    except ValueError as e:
        pytest.fail(f"Failed to parse comma-separated floats from {output_path}: {e}")

    assert len(agent_weights) == 3, f"Expected 3 weights, got {len(agent_weights)}: {agent_weights}"

    true_weights = np.array([2.45012, -1.30400, 0.04599])

    l2_error = np.linalg.norm(agent_weights - true_weights)
    threshold = 1e-4

    assert l2_error <= threshold, (
        f"L2 Error exceeds threshold. "
        f"Measured L2 Error: {l2_error:.6e}, Threshold: {threshold:.6e}. "
        f"Agent weights: {agent_weights}, True weights: {true_weights}"
    )