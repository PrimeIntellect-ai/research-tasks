# test_final_state.py

import os
import json
import pytest

def test_metrics_json_exists():
    """Check if the metrics.json file exists."""
    assert os.path.isfile('/app/metrics.json'), "/app/metrics.json does not exist."

def test_metrics_json_format_and_values():
    """Check the format of metrics.json and validate the metric threshold."""
    with open('/app/metrics.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("metrics.json is not a valid JSON file.")

    required_keys = {"mean", "ci_lower", "ci_upper"}
    missing_keys = required_keys - set(data.keys())
    assert not missing_keys, f"metrics.json is missing keys: {missing_keys}"

    mean_val = float(data['mean'])
    ci_lower = float(data['ci_lower'])
    ci_upper = float(data['ci_upper'])

    assert ci_lower <= mean_val <= ci_upper, f"Confidence interval is invalid: {ci_lower} <= {mean_val} <= {ci_upper} is False"

    target_f0 = 4.25
    error = abs(mean_val - target_f0)
    threshold = 0.05

    assert error <= threshold, f"Absolute error of mean peak frequency ({mean_val}) from target ({target_f0}) is {error:.4f}, which exceeds the threshold of {threshold}."

def test_simulator_compiled():
    """Check if the simulator was compiled to /app/simulator and is executable."""
    assert os.path.isfile('/app/simulator'), "/app/simulator executable does not exist."
    assert os.access('/app/simulator', os.X_OK), "/app/simulator is not executable."

def test_simulator_c_fixed():
    """Check if simulator.c was modified to reduce dt."""
    assert os.path.isfile('/app/simulator.c'), "/app/simulator.c does not exist."
    with open('/app/simulator.c', 'r') as f:
        content = f.read()

    # dt should be <= 0.01, so the original double dt = 0.2; should be gone or changed.
    # We just ensure the original buggy dt is not present, or step size is increased.
    assert "double dt = 0.2;" not in content, "The buggy 'dt = 0.2' is still in simulator.c."