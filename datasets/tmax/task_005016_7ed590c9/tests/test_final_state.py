# test_final_state.py

import os
import pytest

def test_config_file_created():
    config_path = "/home/user/config/collector.conf"
    assert os.path.isfile(config_path), f"Configuration file {config_path} was not created."

    with open(config_path, "r") as f:
        content = f.read().strip()

    assert "ENABLE_PROFILING=true" in content.splitlines(), (
        f"Expected 'ENABLE_PROFILING=true' in {config_path}, but found: {content}"
    )

def test_final_metric_correct():
    metric_path = "/home/user/final_metric.txt"
    assert os.path.isfile(metric_path), f"Output file {metric_path} was not created."

    with open(metric_path, "r") as f:
        content = f.read().strip()

    # The expected value is derived from:
    # Server 1: REQS=150, LATENCY=3
    # Server 2: REQS=200, LATENCY=4
    # WAL TX 1 (Committed): REQS=50, LATENCY=1
    # Total Reqs = 400
    # Total Latency = 8 seconds
    # Average Latency in ms = (8 * 1000) / 400 = 20
    expected_metric = "20"

    assert content == expected_metric, (
        f"Expected final metric to be '{expected_metric}', but got '{content}'. "
        "Ensure spaces in filenames are handled, only committed WAL transactions are processed, "
        "and the latency formula multiplies by 1000 before dividing."
    )