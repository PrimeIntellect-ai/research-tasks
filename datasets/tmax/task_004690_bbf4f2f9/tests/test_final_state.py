# test_final_state.py

import os
import time
import subprocess
import pytest

def test_driver_fixed_exists():
    driver_path = "/home/user/wrapper_repo/driver_fixed.py"
    assert os.path.isfile(driver_path), f"Missing fixed driver script at {driver_path}"

def test_execution_time_and_correctness():
    driver_path = "/home/user/wrapper_repo/driver_fixed.py"
    data_path = "/app/eval_data.json"
    metrics_path = "/home/user/metrics.log"

    # Ensure metrics.log doesn't exist from a previous run or remove it
    if os.path.exists(metrics_path):
        os.remove(metrics_path)

    start_time = time.time()
    res = subprocess.run(
        ["python3", driver_path, data_path],
        capture_output=True
    )
    end_time = time.time()
    actual_time = end_time - start_time

    assert res.returncode == 0, f"Script crashed or failed. stderr: {res.stderr.decode()}"

    assert os.path.isfile(metrics_path), f"Missing metrics log at {metrics_path}"

    with open(metrics_path, "r") as f:
        content = f.read().strip()
        try:
            logged_time = float(content)
        except ValueError:
            pytest.fail(f"Could not parse logged time from {metrics_path}. Content: {content}")

    threshold = 1.5
    assert actual_time < threshold, (
        f"Execution was too slow. Actual time: {actual_time:.3f}s. "
        f"Threshold is {threshold}s. Did you restore the fast-path flag?"
    )