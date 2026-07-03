# test_final_state.py
import os
import json
import pytest

def test_results_json_exists():
    results_file = "/home/user/math_dag/results.json"
    assert os.path.isfile(results_file), f"{results_file} is missing. Did the program run and generate the output?"

def test_results_json_content():
    results_file = "/home/user/math_dag/results.json"

    with open(results_file, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_file} is not valid JSON")

    expected = {
        "A": 10.0,
        "B": 5.0,
        "C": 15.0,
        "D": 150.0,
        "E": 75.0,
        "F": 225.0
    }

    for key, expected_val in expected.items():
        assert key in results, f"Node '{key}' is missing from the results."
        # Use float comparison for safety
        actual_val = float(results[key])
        assert actual_val == expected_val, f"Node '{key}' evaluated incorrectly. Expected {expected_val}, got {actual_val}."