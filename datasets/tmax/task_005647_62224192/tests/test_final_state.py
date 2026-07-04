# test_final_state.py
import os
import json
import math
import pytest

def test_solution_json_exists():
    path = "/home/user/solution.json"
    assert os.path.exists(path), f"File {path} is missing. The task requires creating this file."
    assert os.path.isfile(path), f"Path {path} is not a regular file."

def test_solution_content():
    path = "/home/user/solution.json"
    expected_path = "/tmp/expected_solution.json"

    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.exists(expected_path), f"Expected solution file {expected_path} is missing from the environment."

    with open(path, 'r') as f:
        try:
            solution = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    with open(expected_path, 'r') as f:
        expected = json.load(f)

    assert "optimal_lambda" in solution, "Key 'optimal_lambda' is missing in solution.json."
    assert "max_peak" in solution, "Key 'max_peak' is missing in solution.json."

    assert solution["optimal_lambda"] == expected["optimal_lambda"], \
        f"Incorrect optimal_lambda. Found {solution['optimal_lambda']}, expected {expected['optimal_lambda']}."

    assert math.isclose(solution["max_peak"], expected["max_peak"], abs_tol=1e-4), \
        f"Incorrect max_peak. Found {solution['max_peak']}, expected {expected['max_peak']} (within 1e-4 tolerance)."