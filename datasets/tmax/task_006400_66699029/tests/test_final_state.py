# test_final_state.py

import os
import json
import pytest

def test_params_json_exists_and_correct():
    file_path = "/home/user/params.json"
    assert os.path.isfile(file_path), f"Expected file {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_keys = {"A", "k", "B"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, got {set(data.keys())}"

    assert isinstance(data["A"], (int, float)), "Value for 'A' must be a number."
    assert isinstance(data["k"], (int, float)), "Value for 'k' must be a number."
    assert isinstance(data["B"], (int, float)), "Value for 'B' must be a number."

    assert round(data["A"], 2) == 5.00, f"Expected A to be 5.00, got {data['A']}"
    assert round(data["k"], 2) == 0.20, f"Expected k to be 0.20, got {data['k']}"
    assert round(data["B"], 2) == 1.00, f"Expected B to be 1.00, got {data['B']}"