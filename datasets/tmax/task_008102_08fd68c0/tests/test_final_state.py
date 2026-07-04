# test_final_state.py

import os
import json
import pytest

def test_solution_file_exists():
    solution_path = "/home/user/solution.json"
    assert os.path.exists(solution_path), f"The solution file {solution_path} does not exist."
    assert os.path.isfile(solution_path), f"The path {solution_path} is not a file."

def test_solution_content():
    solution_path = "/home/user/solution.json"
    expected_path = "/home/user/expected_solution.json"

    assert os.path.exists(solution_path), f"Cannot verify content: {solution_path} is missing."
    assert os.path.exists(expected_path), f"Cannot verify content: {expected_path} is missing."

    try:
        with open(solution_path, 'r') as f:
            actual = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {solution_path} does not contain valid JSON.")

    try:
        with open(expected_path, 'r') as f:
            expected = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {expected_path} does not contain valid JSON.")

    assert isinstance(actual, list), f"The solution should be a JSON array, but got {type(actual).__name__}."

    assert actual == expected, (
        f"The content of {solution_path} does not match the expected result.\n"
        f"Expected: {expected}\n"
        f"Got: {actual}"
    )