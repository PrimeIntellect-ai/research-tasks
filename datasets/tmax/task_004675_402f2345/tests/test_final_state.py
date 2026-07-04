# test_final_state.py

import os
import subprocess
import numpy as np
from scipy.stats import wasserstein_distance
import pytest

def test_best_params_exists():
    params_path = "/home/user/best_params.csv"
    assert os.path.exists(params_path), f"Output file not found at {params_path}"
    assert os.path.isfile(params_path), f"Path {params_path} is not a file"

def test_wasserstein_distance_metric():
    params_path = "/home/user/best_params.csv"
    assert os.path.exists(params_path), f"Output file not found at {params_path}"

    with open(params_path, 'r') as f:
        content = f.read().strip()

    # Parse agent's solution
    try:
        params = content.split(',')
        assert len(params) == 3, f"Expected 3 comma-separated values, found {len(params)}"
        alpha, beta, gamma = params[0].strip(), params[1].strip(), params[2].strip()
        float(alpha)
        float(beta)
        float(gamma)
    except Exception as e:
        pytest.fail(f"Failed to parse {params_path}. Ensure it contains exactly 3 comma-separated floats. Error: {e}")

    # Load experimental data
    exp_data_path = "/app/data/experimental_spectrum.txt"
    assert os.path.exists(exp_data_path), f"Experimental data missing at {exp_data_path}"
    exp_data = np.loadtxt(exp_data_path)

    # Run oracle
    binary_path = "/app/bin/spectral_sim"
    assert os.path.exists(binary_path), f"Binary missing at {binary_path}"

    result = subprocess.run([binary_path, alpha, beta, gamma], capture_output=True, text=True)
    assert result.returncode == 0, f"Binary execution failed with return code {result.returncode}. Stderr: {result.stderr}"

    sim_data = np.fromstring(result.stdout, sep=' ')
    assert len(sim_data) == 1024, f"Binary output did not contain 1024 values. Found {len(sim_data)}."

    # Calculate metric
    metric_value = wasserstein_distance(exp_data, sim_data)

    # Verification assertion
    assert metric_value <= 0.15, f"Wasserstein distance {metric_value:.5f} is not <= 0.15. Parameters: alpha={alpha}, beta={beta}, gamma={gamma}"