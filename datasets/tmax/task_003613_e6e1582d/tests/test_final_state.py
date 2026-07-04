# test_final_state.py

import os
import pytest

def test_final_metric_exists_and_correct():
    path = "/home/user/final_metric.txt"
    assert os.path.isfile(path), f"File {path} is missing. The script did not run successfully or output to the correct location."

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {path} is not a valid float: '{content}'")

    assert 15.0 <= val <= 15.2, f"Expected final metric to be approximately 15.1, but got {val}"

def test_analyze_metrics_script_executable():
    path = "/home/user/analyze_metrics.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is no longer executable."