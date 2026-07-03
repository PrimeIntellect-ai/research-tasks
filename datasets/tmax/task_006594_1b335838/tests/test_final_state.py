# test_final_state.py
import os
import json
import pytest

def test_inference_results_exists():
    results_path = '/home/user/inference_results.json'
    assert os.path.exists(results_path), f"Verification failed: {results_path} does not exist."
    assert os.path.isfile(results_path), f"Verification failed: {results_path} is not a file."

def test_inference_results_content():
    results_path = '/home/user/inference_results.json'
    assert os.path.exists(results_path), f"Verification failed: {results_path} does not exist."

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Verification failed: {results_path} does not contain valid JSON.")

    assert 'features' in data, "Verification failed: 'features' key missing in JSON."
    assert 'weights' in data, "Verification failed: 'weights' key missing in JSON."
    assert 'inference_time_ms' in data, "Verification failed: 'inference_time_ms' key missing in JSON."

    expected_features = ['f1', 'f2']
    actual_features = data.get('features')
    assert actual_features == expected_features, f"Verification failed: Expected features {expected_features}, got {actual_features}"

    expected_weights = [-0.0163, 2.4925, -1.2059]
    actual_weights = data.get('weights', [])

    assert len(actual_weights) == 3, f"Verification failed: Incorrect number of weights. Expected 3, got {len(actual_weights)}."

    for expected, actual in zip(expected_weights, actual_weights):
        assert abs(expected - actual) <= 0.001, f"Verification failed: Weight mismatch. Expected ~{expected}, got {actual}"

def test_cleaned_dataset_exists():
    cleaned_path = '/home/user/cleaned_dataset.csv'
    assert os.path.exists(cleaned_path), f"Verification failed: {cleaned_path} does not exist."
    assert os.path.isfile(cleaned_path), f"Verification failed: {cleaned_path} is not a file."

    with open(cleaned_path, 'r') as f:
        header = f.readline().strip().split(',')

    # Check that f3 is removed, but f1, f2, y are present
    assert 'f3' not in header, "Verification failed: 'f3' was not removed from cleaned_dataset.csv."
    assert 'f1' in header, "Verification failed: 'f1' is missing from cleaned_dataset.csv."
    assert 'f2' in header, "Verification failed: 'f2' is missing from cleaned_dataset.csv."
    assert 'y' in header, "Verification failed: 'y' is missing from cleaned_dataset.csv."