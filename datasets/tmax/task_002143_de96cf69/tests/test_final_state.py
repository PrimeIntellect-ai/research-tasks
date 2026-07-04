# test_final_state.py

import os
import json
import pytest

def test_result_json_exists_and_correct():
    result_file = "/home/user/result.json"
    assert os.path.exists(result_file), f"The output file {result_file} was not created."

    with open(result_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {result_file} does not contain valid JSON.")

    # Check schema keys
    expected_keys = {"shortest_path_cost", "total_node_value", "path"}
    assert set(data.keys()) == expected_keys, f"The JSON schema is incorrect. Expected keys: {expected_keys}, Found: {set(data.keys())}"

    # Check types
    assert isinstance(data["shortest_path_cost"], int), "shortest_path_cost must be an integer."
    assert isinstance(data["total_node_value"], int), "total_node_value must be an integer."
    assert isinstance(data["path"], list), "path must be a list of strings."
    assert all(isinstance(x, str) for x in data["path"]), "path must be a list of strings."

    # Check values
    assert data["shortest_path_cost"] == 28, f"Incorrect shortest_path_cost. Expected 28, got {data['shortest_path_cost']}."
    assert data["total_node_value"] == 150, f"Incorrect total_node_value. Expected 150, got {data['total_node_value']}."

    expected_path = ["A", "B", "C", "D", "E"]
    assert data["path"] == expected_path, f"Incorrect path. Expected {expected_path}, got {data['path']}."