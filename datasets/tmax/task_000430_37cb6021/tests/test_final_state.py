# test_final_state.py

import os
import time
import subprocess
import pytest
import numpy as np
from scipy.spatial.distance import pdist, squareform

def test_fast_spec_performance_and_accuracy():
    agent_bin = "/home/user/fast_spec"
    assert os.path.exists(agent_bin), f"Executable not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"{agent_bin} is not executable"

    N = 4000
    M = 1000

    # Generate test data
    np.random.seed(42)
    data = np.random.rand(N, M).astype(np.float32)
    data = data / data.sum(axis=1, keepdims=True)

    test_in = "/tmp/test_large.txt"
    test_out = "/tmp/out_agent.txt"

    # Write input file
    with open(test_in, "w") as f:
        f.write(f"{N} {M}\n")
    # Append the data
    with open(test_in, "ab") as f:
        np.savetxt(f, data, fmt="%.6f", delimiter=" ")

    # Run the agent's binary and measure execution time
    start_time = time.time()
    result = subprocess.run([agent_bin, test_in, test_out], capture_output=True, text=True)
    end_time = time.time()

    assert result.returncode == 0, f"Agent program failed with return code {result.returncode}.\nStderr: {result.stderr}"

    exec_time = end_time - start_time
    assert exec_time <= 3.0, f"Execution time {exec_time:.3f}s exceeded the 3.0s threshold. OpenMP parallelization might be missing or inefficient."

    assert os.path.exists(test_out), f"Agent program did not produce the expected output file at {test_out}"

    # Load agent output
    try:
        agent_dist = np.loadtxt(test_out)
    except Exception as e:
        pytest.fail(f"Failed to load agent output as a numeric matrix: {e}")

    assert agent_dist.shape == (N, N), f"Expected output matrix shape {(N, N)}, but got {agent_dist.shape}"

    # Compute ground truth using highly optimized scipy pdist (Manhattan distance on CDFs)
    cdf = np.cumsum(data, axis=1)
    truth_pdist = pdist(cdf, metric='cityblock')
    truth_dist = squareform(truth_pdist)

    # Calculate MSE
    mse = np.mean((agent_dist - truth_dist) ** 2)

    assert mse <= 1e-8, f"MSE {mse:.2e} exceeds the threshold of 1e-8. The computed distances do not match the expected 1-Wasserstein distance."