# test_final_state.py
import os
import time
import subprocess
import numpy as np

def test_forces_accuracy():
    expected_path = '/home/user/sim/expected_forces.txt'
    actual_path = '/home/user/sim/forces.txt'

    assert os.path.isfile(expected_path), f"Baseline forces file missing at {expected_path}"
    assert os.path.isfile(actual_path), f"Agent forces file missing at {actual_path}"

    baseline = np.loadtxt(expected_path)
    test = np.loadtxt(actual_path)

    assert baseline.shape == test.shape, f"Shape mismatch: expected {baseline.shape}, got {test.shape}"

    mse = np.mean((baseline - test)**2)
    assert mse < 1e-4, f"MSE {mse} is too high (threshold < 1e-4)"

def test_performance():
    exec_path = '/home/user/sim/mesh_sim'
    assert os.path.isfile(exec_path), f"Executable {exec_path} not found. Did you compile it?"

    start_time = time.time()
    result = subprocess.run([exec_path], cwd='/home/user/sim', capture_output=True)
    end_time = time.time()

    assert result.returncode == 0, f"Execution failed with return code {result.returncode}\nStderr: {result.stderr.decode()}"

    agent_time = end_time - start_time

    # Baseline is ~10 seconds. Target is 5x speedup, so < 2.0 seconds.
    # We use 3.0 seconds as a safe upper bound for the optimized version.
    assert agent_time < 3.0, f"Execution time {agent_time:.2f}s is too slow (expected < 3.0s for >= 5x speedup)"