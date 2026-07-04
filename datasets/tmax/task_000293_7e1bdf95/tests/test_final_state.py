# test_final_state.py

import os
import json
import math
import subprocess
import pytest

def get_expected_trace(N, seed):
    """Compute the expected trace using numpy via subprocess to avoid third-party imports in the test."""
    script = f"""
import numpy as np
np.random.seed({seed})
A = np.random.rand({N}, {N})
B = A @ A.T
print(float(np.trace(B)))
"""
    result = subprocess.run(["python3", "-c", script], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())

def test_run_experiments_script_exists_and_executable():
    script_path = "/home/user/workspace/run_experiments.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Bash script {script_path} is not executable."

def test_plots_created():
    plot_dir = "/home/user/workspace/plots"
    assert os.path.isdir(plot_dir), f"Plots directory {plot_dir} is missing."

    for batch_size in [100, 200, 300]:
        plot_file = os.path.join(plot_dir, f"plot_{batch_size}.png")
        assert os.path.isfile(plot_file), f"Plot file {plot_file} is missing."

def test_tracking_jsonl_content():
    tracking_file = "/home/user/results/tracking.jsonl"
    assert os.path.isfile(tracking_file), f"Tracking file {tracking_file} is missing."

    with open(tracking_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {tracking_file}, found {len(lines)}."

    expected_batch_sizes = [100, 200, 300]
    expected_seed = 123

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {tracking_file} is not valid JSON: {line}")

        assert "batch_size" in data, f"Missing 'batch_size' in JSON line {i+1}."
        assert "seed" in data, f"Missing 'seed' in JSON line {i+1}."
        assert "time" in data, f"Missing 'time' in JSON line {i+1}."
        assert "trace" in data, f"Missing 'trace' in JSON line {i+1}."

        batch_size = data["batch_size"]
        assert batch_size == expected_batch_sizes[i], f"Expected batch_size {expected_batch_sizes[i]} in line {i+1}, got {batch_size}."

        seed = data["seed"]
        assert seed == expected_seed, f"Expected seed {expected_seed} in line {i+1}, got {seed}."

        trace = data["trace"]
        expected_trace = get_expected_trace(batch_size, seed)

        assert math.isclose(trace, expected_trace, rel_tol=1e-5), \
            f"Trace value {trace} for batch_size {batch_size} does not match expected {expected_trace}."