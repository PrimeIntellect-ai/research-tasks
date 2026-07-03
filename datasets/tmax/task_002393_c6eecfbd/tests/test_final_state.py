# test_final_state.py

import os
import json
import pytest

def test_results_file_exists():
    results_path = '/home/user/results.json'
    assert os.path.exists(results_path), f"Results file not found at {results_path}"
    assert os.path.isfile(results_path), f"Path {results_path} is not a file"

def test_results_json_content():
    results_path = '/home/user/results.json'
    assert os.path.exists(results_path), "Cannot check content, results.json does not exist."

    try:
        with open(results_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {results_path} is not valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {results_path}: {e}")

    expected_keys = {"slope", "intercept", "mae"}
    actual_keys = set(data.keys())
    missing = expected_keys - actual_keys
    assert not missing, f"results.json is missing keys: {missing}"

    # Verify values (allow small float tolerance due to rounding to 4 decimal places)
    expected_slope = 49.9575
    expected_intercept = 199.7998
    expected_mae = 0.6358

    assert isinstance(data["slope"], (int, float)), "slope must be a number"
    assert isinstance(data["intercept"], (int, float)), "intercept must be a number"
    assert isinstance(data["mae"], (int, float)), "mae must be a number"

    assert abs(data["slope"] - expected_slope) <= 1e-4, \
        f"Expected slope around {expected_slope}, got {data['slope']}"
    assert abs(data["intercept"] - expected_intercept) <= 1e-4, \
        f"Expected intercept around {expected_intercept}, got {data['intercept']}"
    assert abs(data["mae"] - expected_mae) <= 1e-4, \
        f"Expected mae around {expected_mae}, got {data['mae']}"