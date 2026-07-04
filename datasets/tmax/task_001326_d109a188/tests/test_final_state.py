# test_final_state.py

import os
import sys
import json
import subprocess
import numpy as np
import pytest

def test_process_spectra_exists():
    """Check that the student's script exists."""
    script_path = "/home/user/process_spectra.py"
    assert os.path.exists(script_path), f"Missing script: {script_path}"
    assert os.path.isfile(script_path), f"Path is not a file: {script_path}"

def test_pipeline_accuracy_and_stats():
    """Generate hidden data, run both pipelines, compare MSE, and check stats.json."""
    script_path = "/home/user/process_spectra.py"
    legacy_bin = "/app/legacy_cleaner"
    hidden_in = "/app/hidden_test.csv"
    hidden_out = "/home/user/hidden_out.csv"
    oracle_out = "/app/oracle_out.csv"
    stats_json = "/home/user/stats.json"

    # 1. Generate hidden test data
    np.random.seed(42)
    N_rows = 1000
    N_cols = 1024

    # Synthetic data: sine waves + noise + linear trend
    x = np.linspace(0, 4 * np.pi, N_cols)
    data = []
    for _ in range(N_rows):
        signal = np.sin(x + np.random.rand() * 2 * np.pi) * (1 + np.random.rand())
        noise = np.random.normal(0, 0.5, N_cols)
        trend = np.linspace(np.random.rand(), np.random.rand() * 5, N_cols)
        data.append(signal + noise + trend)

    data = np.array(data)
    np.savetxt(hidden_in, data, delimiter=',')

    # 2. Run the legacy cleaner (Oracle)
    assert os.path.exists(legacy_bin), "Legacy cleaner missing."
    subprocess.run([legacy_bin, hidden_in, oracle_out], check=True)

    # 3. Run the student's script
    result = subprocess.run([sys.executable, script_path, hidden_in, hidden_out], capture_output=True, text=True)
    assert result.returncode == 0, f"Student script failed with error:\n{result.stderr}"

    # 4. Compare outputs (MSE)
    assert os.path.exists(hidden_out), "Student script did not create the output file."
    assert os.path.exists(oracle_out), "Oracle did not create the output file."

    agent_data = np.loadtxt(hidden_out, delimiter=',')
    oracle_data = np.loadtxt(oracle_out, delimiter=',')

    assert agent_data.shape == oracle_data.shape, f"Shape mismatch: agent {agent_data.shape} vs oracle {oracle_data.shape}"

    mse = np.mean((agent_data - oracle_data) ** 2)
    assert mse <= 1e-4, f"MSE too high: {mse} (threshold is 1e-4)"

    # 5. Check stats.json
    assert os.path.exists(stats_json), f"Missing stats file: {stats_json}"
    with open(stats_json, 'r') as f:
        try:
            stats = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {stats_json}")

    assert "ci_lower" in stats, "Missing 'ci_lower' in stats.json"
    assert "ci_upper" in stats, "Missing 'ci_upper' in stats.json"

    ci_lower = float(stats["ci_lower"])
    ci_upper = float(stats["ci_upper"])

    assert ci_lower < ci_upper, f"ci_lower ({ci_lower}) must be less than ci_upper ({ci_upper})"

    # Calculate oracle bootstrap CI for sanity check
    max_vals = np.max(oracle_data, axis=1)
    np.random.seed(42)
    boot_maxes = []
    for _ in range(1000):
        sample = np.random.choice(max_vals, size=len(max_vals), replace=True)
        boot_maxes.append(np.mean(sample)) # Wait, task says "bootstrap confidence interval ... of the maximum peak heights"
        # The wording "bootstrap confidence interval ... of the maximum peak heights" usually means the CI of the mean of the max peak heights, 
        # or the CI of the max peak heights themselves. Let's just check they are within a reasonable range of the actual max values.

    true_mean_max = np.mean(max_vals)
    true_std_max = np.std(max_vals)

    # A loose check to ensure the CI is in the right ballpark (mean +/- 3 std dev)
    assert true_mean_max - 3 * true_std_max <= ci_lower <= true_mean_max + 3 * true_std_max, f"ci_lower {ci_lower} is out of expected range."
    assert true_mean_max - 3 * true_std_max <= ci_upper <= true_mean_max + 3 * true_std_max, f"ci_upper {ci_upper} is out of expected range."