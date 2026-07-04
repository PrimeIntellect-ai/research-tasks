# test_final_state.py
import os
import numpy as np
import pytest

def test_sim_dist_mae():
    # Define ground truth model
    N = 300
    np.random.seed(42)  # For reproducibility in the test
    t = np.random.uniform(0, N, 1000000)
    mu = 128
    A = 40
    f = 5.0 / N
    noise = np.random.uniform(-5.0, 5.0, 1000000)
    S = mu + A * np.cos(2 * np.pi * f * t) + noise

    # Empirical min/max (approximate without noise is 88 to 168)
    min_val = 88.0
    max_val = 168.0

    truth_hist, _ = np.histogram(S, bins=10, range=(min_val, max_val), density=True)
    truth_probs = truth_hist * ((max_val - min_val) / 10.0)

    # Check if agent output exists
    output_path = '/home/user/sim_dist.txt'
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    # Read agent probabilities
    with open(output_path, 'r') as f_in:
        lines = f_in.read().split()

    agent_probs = []
    for x in lines:
        if x.strip() != '':
            try:
                agent_probs.append(float(x))
            except ValueError:
                pytest.fail(f"Could not parse '{x}' as a float in {output_path}.")

    agent_probs = np.array(agent_probs)

    assert len(agent_probs) == 10, f"Output must contain exactly 10 lines/values, found {len(agent_probs)}."

    # Calculate MAE
    mae = np.mean(np.abs(truth_probs - agent_probs))

    # Assert threshold
    threshold = 0.05
    assert mae < threshold, f"FAILURE: MAE={mae:.4f} is above the {threshold} threshold."