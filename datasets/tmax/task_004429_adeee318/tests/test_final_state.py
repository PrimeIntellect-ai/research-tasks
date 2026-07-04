# test_final_state.py
import os
import json
import pytest

def test_deadlock_json_exists_and_correct():
    json_path = "/home/user/deadlock.json"
    assert os.path.isfile(json_path), f"The file {json_path} does not exist. Did you run your C++ program?"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert isinstance(data, list), f"The JSON in {json_path} should be an array."
    assert data == [13, 14], f"The cycle detected is incorrect. Expected [13, 14], got {data}."

def test_solve_cpp_exists():
    cpp_path = "/home/user/solve.cpp"
    assert os.path.isfile(cpp_path), f"The file {cpp_path} does not exist. You must write your solution in this file."