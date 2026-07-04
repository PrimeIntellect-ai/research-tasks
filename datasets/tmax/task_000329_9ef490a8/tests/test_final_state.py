# test_final_state.py
import os
import subprocess
import numpy as np
import pytest

def test_reconstructed_inputs_exists():
    path = "/home/user/reconstructed_inputs.csv"
    assert os.path.exists(path), f"Missing reconstructed inputs file at {path}"
    assert os.path.isfile(path), f"{path} is not a file"
    assert os.path.getsize(path) > 0, f"{path} is empty"

def test_safe_aggregator_exists_and_executable():
    path = "/home/user/safe_aggregator.sh"
    assert os.path.exists(path), f"Missing safe aggregator script at {path}"
    assert os.path.isfile(path), f"{path} is not a file"
    assert os.access(path, os.X_OK), f"Safe aggregator script at {path} is not executable"

def test_safe_aggregator_accuracy():
    script_path = "/home/user/safe_aggregator.sh"
    test_file = "/tmp/held_out.txt"

    # Generate held-out test data
    vals = [10000000.0] + [0.015] * 50000
    np.random.shuffle(vals)
    with open(test_file, 'w') as f:
        for v in vals:
            f.write(f"{v}\n")

    true_sum = sum(vals) # 64-bit float precision sum in Python

    # Run agent wrapper
    result = subprocess.run([script_path, test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    try:
        agent_sum = float(result.stdout.strip())
    except ValueError:
        pytest.fail(f"Could not parse script output as float. Output was: {result.stdout!r}")

    absolute_error = abs(true_sum - agent_sum)

    # Threshold check
    assert absolute_error < 50.0, (
        f"Absolute error {absolute_error} is too high! Expected < 50.0. "
        f"True sum: {true_sum}, Agent sum: {agent_sum}. "
        "Did you sort the values by magnitude before summing?"
    )