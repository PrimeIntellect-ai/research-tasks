# test_final_state.py

import os
import re
import subprocess
import pytest

def get_true_mse():
    """
    Run the oracle binary to get the exact expected OOB MSE.
    Fallback to 2.4512 if it fails or cannot be parsed.
    """
    oracle_path = "/app/oracle_pipeline"
    if os.path.isfile(oracle_path) and os.access(oracle_path, os.X_OK):
        try:
            result = subprocess.run([oracle_path], capture_output=True, text=True, check=True)
            floats = re.findall(r"[-+]?\d*\.\d+", result.stdout)
            if floats:
                return float(floats[-1])
        except Exception:
            pass
    return 2.4512

def test_fixed_binary_exists():
    fixed_bin = "/home/user/bin/train_model_fixed"
    assert os.path.isfile(fixed_bin), f"Fixed binary is missing: {fixed_bin}"
    assert os.access(fixed_bin, os.X_OK), f"Fixed binary is not executable: {fixed_bin}"

def test_metrics_file_and_accuracy():
    metrics_file = "/home/user/metrics.txt"
    assert os.path.isfile(metrics_file), f"Metrics file is missing: {metrics_file}"

    with open(metrics_file, 'r') as f:
        content = f.read().strip()

    try:
        agent_val = float(content)
    except ValueError:
        pytest.fail(f"Metrics file does not contain a valid float. Found: '{content}'")

    true_val = get_true_mse()
    diff = abs(agent_val - true_val)

    threshold = 0.05
    assert diff <= threshold, (
        f"Agent MSE ({agent_val}) differs from True MSE ({true_val}) "
        f"by {diff}, which exceeds the threshold of {threshold}."
    )