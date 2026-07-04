# test_final_state.py

import os
import json
import pytest

def test_results_json_exists_and_format():
    results_file = "/home/user/results.json"
    assert os.path.exists(results_file), f"Missing {results_file}"

    with open(results_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_file} is not valid JSON")

    expected_keys = {"w0", "w1", "w0_lower", "w0_upper", "w1_lower", "w1_upper"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}"

    for k, v in data.items():
        assert isinstance(v, (int, float)), f"Value for {k} must be a number"

def test_results_values():
    results_file = "/home/user/results.json"
    if not os.path.exists(results_file):
        pytest.skip("Results file missing")

    with open(results_file, 'r') as f:
        data = json.load(f)

    # Read graph and y to compute expected GD result
    # We use basic python math to avoid numpy dependency if possible, but numpy is standard in data science tasks.
    # Since we can use standard library only, we will just check if the values are reasonably close to the ground truth.
    # The ground truth w was approximately [2.5, -1.5] (up to sign flips due to eigenvector signs).

    w0 = data["w0"]
    w1 = data["w1"]

    # Check magnitude of w0 and w1 (allowing for sign flips from eigendecomposition)
    assert abs(abs(w0) - 2.5) < 0.5, f"w0 magnitude {abs(w0)} is too far from expected ~2.5"
    assert abs(abs(w1) - 1.5) < 0.5, f"w1 magnitude {abs(w1)} is too far from expected ~1.5"

    # Check bounds logic
    assert data["w0_lower"] <= w0 <= data["w0_upper"], "w0 must be within its bootstrap bounds"
    assert data["w1_lower"] <= w1 <= data["w1_upper"], "w1 must be within its bootstrap bounds"

    # Check bound widths (should be relatively small but > 0)
    w0_width = data["w0_upper"] - data["w0_lower"]
    w1_width = data["w1_upper"] - data["w1_lower"]

    assert 0.01 < w0_width < 1.0, f"w0 bound width {w0_width} is unreasonable"
    assert 0.01 < w1_width < 1.0, f"w1 bound width {w1_width} is unreasonable"