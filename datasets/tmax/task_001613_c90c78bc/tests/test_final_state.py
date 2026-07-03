# test_final_state.py

import os
import json
import pytest

def test_results_file_exists():
    path = "/home/user/results/gaps.json"
    assert os.path.isfile(path), f"{path} does not exist. Did you create the results directory and output file?"

def test_results_content_and_sorting():
    path = "/home/user/results/gaps.json"
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} does not contain valid JSON.")

    expected = [
        {"x": "N3", "y": "N1", "z": "N2"},
        {"x": "N3", "y": "N1", "z": "N4"},
        {"x": "N5", "y": "N6", "z": "N7"}
    ]

    assert isinstance(data, list), "The root of the JSON file must be an array."

    # Check that keys are exactly "x", "y", "z" for each object
    for i, item in enumerate(data):
        assert isinstance(item, dict), f"Element at index {i} is not a JSON object."
        assert set(item.keys()) == {"x", "y", "z"}, f"Element at index {i} has incorrect keys: {list(item.keys())}. Expected exactly ['x', 'y', 'z']."

    # The list must match exactly, which also validates the sorting requirement
    assert data == expected, f"Output JSON data does not match the expected result or is not sorted correctly.\nExpected: {expected}\nGot: {data}"