# test_final_state.py

import os
import json
import numpy as np
import pytest

def test_output_file_exists():
    path = "/workspace/output.txt"
    assert os.path.isfile(path), f"Output file {path} is missing. Did you successfully compile and run the program?"

def test_stddev_accuracy():
    logs_path = "/workspace/logs.json"
    output_path = "/workspace/output.txt"

    assert os.path.isfile(logs_path), f"Log file {logs_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    # Load ground truth data
    with open(logs_path, 'r') as f:
        data = json.load(f)

    latencies = [item["latency"] for item in data if "latency" in item]
    assert len(latencies) > 0, "No latencies found in logs.json"

    # Calculate expected stddev (population stddev, ddof=0)
    expected_stddev = np.std(latencies, dtype=np.float64, ddof=0)

    # Read agent's output
    with open(output_path, 'r') as f:
        output_str = f.read().strip()

    try:
        agent_stddev = float(output_str)
    except ValueError:
        pytest.fail(f"Could not parse output in {output_path} as a float. Got: '{output_str}'")

    # Calculate absolute error
    abs_error = abs(expected_stddev - agent_stddev)

    # Assert metric threshold
    threshold = 1e-12
    assert abs_error <= threshold, (
        f"Precision loss detected or incorrect calculation! "
        f"Expected stddev: {expected_stddev}, Agent stddev: {agent_stddev}. "
        f"Absolute Error: {abs_error} (Threshold: <= {threshold})"
    )