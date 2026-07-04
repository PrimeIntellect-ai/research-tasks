# test_final_state.py

import os
import json
import math
import pytest

def test_solution_file_exists():
    """Check if the solution.json file exists."""
    file_path = "/home/user/solution.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The Go program may not have run or failed to output."

def test_solution_contents_match():
    """Check if the solution matches the expected ground truth within tolerance."""
    solution_path = "/home/user/solution.json"
    expected_path = "/home/user/expected_solution.json"

    assert os.path.isfile(expected_path), f"Expected solution file {expected_path} is missing."
    assert os.path.isfile(solution_path), f"Solution file {solution_path} is missing."

    with open(solution_path, 'r') as f:
        try:
            agent_ans = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {solution_path} is not valid JSON.")

    with open(expected_path, 'r') as f:
        truth_ans = json.load(f)

    assert isinstance(agent_ans, list), f"Expected a JSON array in {solution_path}, got {type(agent_ans).__name__}."
    assert len(agent_ans) == len(truth_ans), f"Expected {len(truth_ans)} elements, got {len(agent_ans)}."

    for i, (a, t) in enumerate(zip(agent_ans, truth_ans)):
        assert isinstance(a, (int, float)), f"Element at index {i} is not a number: {a}"
        assert math.isclose(a, t, rel_tol=1e-4, abs_tol=1e-4), f"Value at index {i} does not match. Expected {t}, got {a}."