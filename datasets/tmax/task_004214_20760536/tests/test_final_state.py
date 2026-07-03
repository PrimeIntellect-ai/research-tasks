# test_final_state.py

import os
import json
import math
import pytest

def test_model_metrics_json_exists():
    json_path = "/home/user/model_metrics.json"
    assert os.path.isfile(json_path), f"Output file does not exist: {json_path}"

def test_model_metrics_contents():
    json_path = "/home/user/model_metrics.json"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "intercept" in data, "Missing 'intercept' in JSON output."
    assert "weights" in data, "Missing 'weights' in JSON output."
    assert "avg_inference_micros" in data, "Missing 'avg_inference_micros' in JSON output."

    expected_intercept = 2.5
    expected_weights = [1.5, -0.8, 0.4]

    assert isinstance(data["intercept"], (int, float)), "Intercept must be a number."
    assert math.isclose(data["intercept"], expected_intercept, rel_tol=1e-3, abs_tol=1e-3), \
        f"Intercept mismatch: expected {expected_intercept}, got {data['intercept']}"

    assert isinstance(data["weights"], list), "Weights must be an array."
    assert len(data["weights"]) == 3, f"Weights array must have exactly 3 elements, got {len(data['weights'])}"

    for i, w in enumerate(expected_weights):
        assert isinstance(data["weights"][i], (int, float)), f"Weight at index {i} must be a number."
        assert math.isclose(data["weights"][i], w, rel_tol=1e-3, abs_tol=1e-3), \
            f"Weight {i} mismatch: expected {w}, got {data['weights'][i]}"

    assert isinstance(data["avg_inference_micros"], (int, float)), "avg_inference_micros must be a number."
    assert data["avg_inference_micros"] >= 0, "avg_inference_micros must be non-negative."