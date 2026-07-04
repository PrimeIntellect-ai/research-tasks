# test_final_state.py

import os
import json
import random
import numpy as np
import pytest

def test_simulate_script_fixed():
    path = "/app/montecarlo-pi-mpi-1.0.0/simulate.py"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "op=MPI.SUM" in content, f"The script {path} should have been fixed to use MPI.SUM."

def test_bootstrap_results_metric():
    results_path = "/home/user/bootstrap_results.json"
    assert os.path.exists(results_path), f"File {results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file bootstrap_results.json is not valid JSON.")

    assert "mean_estimate" in agent_data, "Missing 'mean_estimate' in JSON."
    assert "ci_lower" in agent_data, "Missing 'ci_lower' in JSON."
    assert "ci_upper" in agent_data, "Missing 'ci_upper' in JSON."

    agent_mean = float(agent_data["mean_estimate"])
    agent_lower = float(agent_data["ci_lower"])
    agent_upper = float(agent_data["ci_upper"])

    # Recompute ground truth
    expected_estimates = []
    for run_index in range(50):
        total_inside = 0
        for rank in range(4):
            random.seed(run_index + rank * 1000)
            for _ in range(2500):
                x = random.random()
                y = random.random()
                if x*x + y*y <= 1.0:
                    total_inside += 1
        pi_est = 4.0 * total_inside / 10000.0
        expected_estimates.append(pi_est)

    expected_estimates = np.array(expected_estimates)

    np.random.seed(42)
    bootstrapped_means = []
    for _ in range(10000):
        sample = np.random.choice(expected_estimates, size=50, replace=True)
        bootstrapped_means.append(np.mean(sample))

    true_mean = float(np.mean(expected_estimates))
    true_lower = float(np.percentile(bootstrapped_means, 2.5))
    true_upper = float(np.percentile(bootstrapped_means, 97.5))

    max_error = max(
        abs(agent_mean - true_mean),
        abs(agent_lower - true_lower),
        abs(agent_upper - true_upper)
    )

    assert max_error <= 1e-4, (
        f"MAE {max_error} exceeds threshold 1e-4.\n"
        f"Expected: mean={true_mean}, lower={true_lower}, upper={true_upper}\n"
        f"Got: mean={agent_mean}, lower={agent_lower}, upper={agent_upper}"
    )