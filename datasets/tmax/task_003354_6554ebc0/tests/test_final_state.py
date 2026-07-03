# test_final_state.py
import os
import json
import math

def test_results_json_exists():
    file_path = '/home/user/results.json'
    assert os.path.isfile(file_path), f"File {file_path} is missing."

def test_results_json_content():
    file_path = '/home/user/results.json'
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} is not valid JSON."

    expected_keys = {"alpha", "kl_divergence", "wasserstein_distance"}
    assert set(data.keys()) == expected_keys, f"Expected keys {expected_keys}, got {set(data.keys())}"

    expected_values = {
        "alpha": 4.672909,
        "kl_divergence": 0.005166,
        "wasserstein_distance": 0.223030
    }

    for key, expected in expected_values.items():
        actual = data[key]
        assert isinstance(actual, (int, float)), f"Value for {key} must be a number, got {type(actual)}"
        assert math.isclose(actual, expected, abs_tol=1e-4), \
            f"Expected {key} to be close to {expected}, got {actual}"