# test_final_state.py

import os
import pytest
import subprocess

def test_shared_library_built():
    so_path = "/home/user/math_optimizer/libmathops.so"
    assert os.path.isfile(so_path), f"Shared library not built at {so_path}"

def test_metric_file_exists_and_threshold_met():
    metric_path = "/home/user/math_optimizer/metric.txt"
    assert os.path.isfile(metric_path), f"Metric file not found at {metric_path}"

    with open(metric_path, 'r') as f:
        content = f.read().strip()

    try:
        execution_time = float(content)
    except ValueError:
        pytest.fail(f"Could not parse execution time as float from {metric_path}. Content: {content}")

    threshold = 0.5
    assert execution_time <= threshold, f"Execution time {execution_time} is not <= {threshold}. Optimization flags (-O3) might be missing in the Makefile."

def test_test_ops_runs_successfully():
    test_script = "/home/user/math_optimizer/test_ops.py"
    assert os.path.isfile(test_script), f"Test script missing at {test_script}"

    # Run the test script to ensure it passes
    result = subprocess.run(
        ["python3", test_script],
        cwd="/home/user/math_optimizer",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"test_ops.py failed to run. stdout:\n{result.stdout}\nstderr:\n{result.stderr}"