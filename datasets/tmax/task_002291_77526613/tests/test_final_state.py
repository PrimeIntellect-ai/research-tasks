# test_final_state.py
import os
import json

def test_model_results_exists():
    """Test that the output JSON file exists."""
    file_path = '/home/user/model_results.json'
    assert os.path.isfile(file_path), f"File not found: {file_path}"

def test_model_results_content():
    """Test that the output JSON contains the correct keys and values within expected bounds."""
    file_path = '/home/user/model_results.json'

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} is not valid JSON."

    expected_keys = {"a", "b", "c", "optimal_C"}
    actual_keys = set(data.keys())
    assert actual_keys == expected_keys, f"Expected keys {expected_keys}, but got {actual_keys}"

    try:
        a = float(data['a'])
        b = float(data['b'])
        c = float(data['c'])
        opt_c = float(data['optimal_C'])
    except (ValueError, TypeError):
        assert False, "All values in the JSON must be numbers."

    # Check bounds (accounting for noise in generation)
    assert 0.45 <= a <= 0.55, f"Parameter 'a' out of bounds: {a}. Expected around 0.5."
    assert 1.9 <= b <= 2.1, f"Parameter 'b' out of bounds: {b}. Expected around 2.0."
    assert 1.45 <= c <= 1.55, f"Parameter 'c' out of bounds: {c}. Expected around 1.5."
    assert 36.5 <= opt_c <= 38.0, f"Optimal C out of bounds: {opt_c}. Expected around 37.28."