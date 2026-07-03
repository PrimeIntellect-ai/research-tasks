# test_final_state.py

import os
import json
import pytest

RESULTS_JSON = "/home/user/pipeline_results.json"

def test_pipeline_results_exists():
    """Verify that the pipeline_results.json file has been created."""
    assert os.path.isfile(RESULTS_JSON), f"Expected output file {RESULTS_JSON} is missing."

def test_pipeline_results_format_and_values():
    """Verify the contents of pipeline_results.json."""
    with open(RESULTS_JSON, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULTS_JSON} is not a valid JSON file.")

    # Check required keys
    expected_keys = {"store_id_dtype", "base_accuracy", "ci_lower", "ci_upper"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"Missing keys in JSON output: {missing_keys}"

    # Check data types
    assert data["store_id_dtype"] == "int64", f"Expected store_id_dtype to be 'int64', got {data['store_id_dtype']}"

    # Verify numeric values within an epsilon of 0.01
    epsilon = 0.01

    # Expected values based on the canonical truth
    expected_base_accuracy = 0.82
    expected_ci_lower = 0.765
    expected_ci_upper = 0.87

    assert isinstance(data["base_accuracy"], (int, float)), "base_accuracy must be a number"
    assert isinstance(data["ci_lower"], (int, float)), "ci_lower must be a number"
    assert isinstance(data["ci_upper"], (int, float)), "ci_upper must be a number"

    assert abs(data["base_accuracy"] - expected_base_accuracy) <= epsilon, \
        f"base_accuracy {data['base_accuracy']} is not within {epsilon} of expected {expected_base_accuracy}"

    assert abs(data["ci_lower"] - expected_ci_lower) <= epsilon, \
        f"ci_lower {data['ci_lower']} is not within {epsilon} of expected {expected_ci_lower}"

    assert abs(data["ci_upper"] - expected_ci_upper) <= epsilon, \
        f"ci_upper {data['ci_upper']} is not within {epsilon} of expected {expected_ci_upper}"