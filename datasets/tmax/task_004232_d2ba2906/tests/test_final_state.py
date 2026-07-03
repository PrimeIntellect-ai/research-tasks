# test_final_state.py
import os
import json
import pytest

def test_results_json_exists_and_correct():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"The file {results_path} does not exist. The Rust program may not have created it."

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {results_path} does not contain valid JSON.")

    expected = [20, 99, 10, 30, 100]

    assert isinstance(data, list), f"The JSON in {results_path} should be a list, but got {type(data).__name__}."
    assert data == expected, f"The results in {results_path} are incorrect. Expected {expected}, but got {data}."