# test_final_state.py

import os
import json
import math
import struct
import pytest

def test_artifact_metrics_json_exists():
    output_path = "/home/user/artifact_metrics.json"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did you run the compiled C program?"

def test_artifact_metrics_values():
    output_path = "/home/user/artifact_metrics.json"
    assert os.path.isfile(output_path), "Output file missing."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON.")

    assert "mean" in data, "Missing 'mean' key in JSON output."
    assert "ci_lower" in data, "Missing 'ci_lower' key in JSON output."
    assert "ci_upper" in data, "Missing 'ci_upper' key in JSON output."

    # Compute expected values from the binary file directly to be robust
    weights_path = "/home/user/weights.bin"
    assert os.path.isfile(weights_path), f"Missing file: {weights_path}"

    with open(weights_path, 'rb') as f:
        binary_data = f.read()

    # 10000 doubles
    n = 10000
    assert len(binary_data) == n * 8, "Weights file size is incorrect."

    values = struct.unpack(f"{n}d", binary_data)

    expected_mean = sum(values) / n
    expected_variance = sum((x - expected_mean) ** 2 for x in values) / n
    expected_stddev = math.sqrt(expected_variance)
    expected_margin = 1.96 * (expected_stddev / math.sqrt(n))

    expected_ci_lower = expected_mean - expected_margin
    expected_ci_upper = expected_mean + expected_margin

    # The C code formats to 6 decimal places, so we check within 1e-5
    assert math.isclose(data["mean"], expected_mean, abs_tol=1e-5), \
        f"Expected mean ~{expected_mean:.6f}, got {data['mean']}"

    assert math.isclose(data["ci_lower"], expected_ci_lower, abs_tol=1e-5), \
        f"Expected ci_lower ~{expected_ci_lower:.6f}, got {data['ci_lower']}"

    assert math.isclose(data["ci_upper"], expected_ci_upper, abs_tol=1e-5), \
        f"Expected ci_upper ~{expected_ci_upper:.6f}, got {data['ci_upper']}"