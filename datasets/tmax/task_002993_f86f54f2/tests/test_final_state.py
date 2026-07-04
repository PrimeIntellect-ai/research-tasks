# test_final_state.py

import os
import json
import pytest

def test_cov_json_exists():
    """Check that the output JSON file exists."""
    output_file = "/home/user/mcmc/cov.json"
    assert os.path.exists(output_file), f"Missing required output file: {output_file}"
    assert os.path.isfile(output_file), f"Expected a file at {output_file}"

def test_cov_json_format_and_keys():
    """Check that the JSON file has the correct keys and numeric values."""
    output_file = "/home/user/mcmc/cov.json"

    try:
        with open(output_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {output_file} is not valid JSON.")

    expected_keys = {"var_x", "var_y", "cov_xy"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"JSON file is missing keys: {missing_keys}"

    for key in expected_keys:
        assert isinstance(data[key], (int, float)), f"Value for {key} must be a number, got {type(data[key])}"

def test_covariance_accuracy():
    """Evaluate the accuracy of the estimated covariance matrix using SSE."""
    output_file = "/home/user/mcmc/cov.json"

    with open(output_file, 'r') as f:
        data = json.load(f)

    true_var_x = 5.0 / 14.0
    true_var_y = 3.0 / 14.0
    true_cov_xy = 1.0 / 14.0

    sse = (data['var_x'] - true_var_x)**2 + \
          (data['var_y'] - true_var_y)**2 + \
          (data['cov_xy'] - true_cov_xy)**2

    threshold = 0.001

    assert sse <= threshold, (
        f"Sum of Squared Errors (SSE) is too high. "
        f"Got SSE={sse:.6f}, expected <={threshold}. "
        f"Estimated: var_x={data['var_x']}, var_y={data['var_y']}, cov_xy={data['cov_xy']}. "
        f"True: var_x={true_var_x}, var_y={true_var_y}, cov_xy={true_cov_xy}."
    )