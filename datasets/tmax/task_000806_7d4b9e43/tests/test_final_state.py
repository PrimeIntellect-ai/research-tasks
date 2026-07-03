# test_final_state.py
import os
import json
import pytest

def test_results_json_exists_and_valid():
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"Missing output file: {results_path}"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    assert "estimated_gravity" in results, "Missing 'estimated_gravity' in results.json"
    assert "trajectory_coefficients" in results, "Missing 'trajectory_coefficients' in results.json"
    assert "optimization_steps_taken" in results, "Missing 'optimization_steps_taken' in results.json"

    try:
        estimated_gravity = float(results["estimated_gravity"])
    except ValueError:
        pytest.fail(f"'estimated_gravity' must be a number, got: {results['estimated_gravity']}")

    # Calculate absolute percentage error
    true_gravity = 9.81
    error = abs(estimated_gravity - true_gravity) / true_gravity

    assert error <= 0.05, f"Estimated gravity {estimated_gravity} is too far from true value {true_gravity} (Error: {error:.4f}, Threshold: 0.05)"