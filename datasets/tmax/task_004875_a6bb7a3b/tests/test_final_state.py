# test_final_state.py
import os
import json
import math

def test_results_json_exists():
    """Check if results.json exists."""
    file_path = '/home/user/results.json'
    assert os.path.exists(file_path), f"File {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_results_json_structure_and_values():
    """Check the structure and values of results.json."""
    file_path = '/home/user/results.json'
    with open(file_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{file_path} is not a valid JSON file."

    expected_keys = {"a", "b", "c", "d", "optimal_x0", "optimal_y0", "max_integral"}
    actual_keys = set(results.keys())
    assert expected_keys.issubset(actual_keys), f"Missing keys in JSON. Expected {expected_keys}, found {actual_keys}."

    # Check parameters
    assert math.isclose(results['a'], 0.5, abs_tol=0.05), f"Parameter 'a' is incorrect. Expected ~0.5, got {results['a']}."
    assert math.isclose(results['b'], 0.2, abs_tol=0.05), f"Parameter 'b' is incorrect. Expected ~0.2, got {results['b']}."
    assert math.isclose(results['c'], 0.8, abs_tol=0.05), f"Parameter 'c' is incorrect. Expected ~0.8, got {results['c']}."
    assert math.isclose(results['d'], 0.3, abs_tol=0.05), f"Parameter 'd' is incorrect. Expected ~0.3, got {results['d']}."

    # Check optimal initial conditions
    assert math.isclose(results['optimal_x0'], 5.0, abs_tol=0.05), f"'optimal_x0' is incorrect. Expected ~5.0, got {results['optimal_x0']}."
    assert math.isclose(results['optimal_y0'], 5.0, abs_tol=0.05), f"'optimal_y0' is incorrect. Expected ~5.0, got {results['optimal_y0']}."

    # Check max_integral
    assert 80.0 < results['max_integral'] < 95.0, f"'max_integral' out of expected bounds (80.0 - 95.0). Got {results['max_integral']}."