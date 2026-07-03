# test_final_state.py

import os
import glob
import subprocess
import pytest
import numpy as np

def test_ssh_works():
    """Verify that SSH to localhost works without a password prompt."""
    try:
        result = subprocess.run(
            ["ssh", "-q", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=no", "localhost", "echo", "OK"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert "OK" in result.stdout.strip(), f"SSH to localhost failed. stdout: '{result.stdout}', stderr: '{result.stderr}'"
    except subprocess.TimeoutExpired:
        pytest.fail("SSH command timed out. Ensure SSH is configured correctly to not prompt for a password.")
    except Exception as e:
        pytest.fail(f"SSH command failed with exception: {e}")

def test_logrotate_config():
    """Verify that log rotation is configured for the target service's usage.log with a daily interval."""
    target_log = "/var/log/services/caching-service/usage.log"
    found = False

    # Check in /etc/logrotate.d/
    logrotate_dir = "/etc/logrotate.d"
    if os.path.isdir(logrotate_dir):
        for fname in os.listdir(logrotate_dir):
            filepath = os.path.join(logrotate_dir, fname)
            if os.path.isfile(filepath):
                with open(filepath, "r") as f:
                    content = f.read()
                    if target_log in content and "daily" in content:
                        found = True
                        break

    # Check in /etc/logrotate.conf if not found in /etc/logrotate.d/
    if not found and os.path.isfile("/etc/logrotate.conf"):
        with open("/etc/logrotate.conf", "r") as f:
            content = f.read()
            if target_log in content and "daily" in content:
                found = True

    assert found, f"Could not find a logrotate configuration for {target_log} specifying 'daily' rotation."

def test_analyze_script_exists():
    """Verify that the analyze.sh script exists and is executable."""
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Missing analyze script: {script_path}"

def test_prediction_metric():
    """Verify the prediction value using the metric threshold (MSE <= 1.0)."""
    pred_file = "/home/user/prediction.txt"
    assert os.path.isfile(pred_file), f"Missing prediction file: {pred_file}"

    with open(pred_file, "r") as f:
        pred_str = f.read().strip()

    try:
        pred = float(pred_str)
    except ValueError:
        pytest.fail(f"The file {pred_file} does not contain a valid floating-point number. Found: '{pred_str}'")

    # Re-derive the exact reference linear regression from the actual logs
    log_files = glob.glob("/var/log/services/caching-service/usage.log*")
    assert log_files, "No log files found for caching-service to calculate reference."

    t_vals = []
    cpu_vals = []
    for lf in log_files:
        with open(lf, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    try:
                        t = float(parts[0])
                        cpu = float(parts[1])
                        t_vals.append(t)
                        cpu_vals.append(cpu)
                    except ValueError:
                        continue

    assert len(t_vals) > 1, "Not enough valid data points found in the logs to perform linear regression."

    t_vals = np.array(t_vals)
    cpu_vals = np.array(cpu_vals)

    # Calculate linear regression: CPU = m * T + c
    A = np.vstack([t_vals, np.ones(len(t_vals))]).T
    m, c = np.linalg.lstsq(A, cpu_vals, rcond=None)[0]

    ref = m * 100 + c
    mse = (pred - ref)**2

    assert mse <= 1.0, f"Predicted value {pred} is too far from reference {ref:.2f}. MSE={mse:.4f} (Threshold <= 1.0)"