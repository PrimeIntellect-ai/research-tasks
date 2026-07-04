# test_final_state.py

import json
import os
import pytest

def test_results_file_exists_and_structure():
    path = '/home/user/results.json'
    assert os.path.exists(path), f"Expected results file at {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    expected_keys = {'polynomial_coefficients', 'threshold', 'divergent_trajectory_ids'}
    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"Missing keys in results.json: {missing_keys}"

def test_results_values():
    path = '/home/user/results.json'
    with open(path, 'r') as f:
        results = json.load(f)

    # Check polynomial_coefficients
    coeffs = results.get('polynomial_coefficients')
    assert isinstance(coeffs, list), "polynomial_coefficients must be a list."
    assert len(coeffs) == 4, f"Expected 4 polynomial_coefficients, got {len(coeffs)}."
    assert all(isinstance(x, (int, float)) for x in coeffs), "All polynomial_coefficients must be numbers."

    # Check threshold
    threshold = results.get('threshold')
    assert isinstance(threshold, (int, float)), "threshold must be a number."
    assert 1.0 < threshold < 5.0, f"threshold {threshold} is outside the expected reasonable range."

    # Check divergent_trajectory_ids
    div_ids = results.get('divergent_trajectory_ids')
    assert isinstance(div_ids, list), "divergent_trajectory_ids must be a list."

    expected_div_ids = [2, 7, 14, 23, 31, 38, 45]
    assert div_ids == expected_div_ids, f"Expected divergent_trajectory_ids {expected_div_ids}, but got {div_ids}."