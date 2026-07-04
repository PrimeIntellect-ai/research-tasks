# test_final_state.py
import json
import os
import pytest

def test_deadlocks_json_exists_and_correct():
    file_path = "/home/user/deadlocks.json"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected = [
        {"cycle_nodes": ["DS1", "DS2", "DS3"], "researchers": ["Alice", "Bob"]},
        {"cycle_nodes": ["DS4", "DS5", "DS6"], "researchers": ["Charlie", "Dave", "Eve"]}
    ]

    assert isinstance(data, list), "The JSON root must be a list."
    assert len(data) == len(expected), f"Expected {len(expected)} cycles, found {len(data)}."

    for i, expected_obj in enumerate(expected):
        actual_obj = data[i]
        assert isinstance(actual_obj, dict), f"Item at index {i} is not a JSON object (dictionary)."

        assert "cycle_nodes" in actual_obj, f"Item at index {i} is missing 'cycle_nodes' key."
        assert "researchers" in actual_obj, f"Item at index {i} is missing 'researchers' key."

        assert actual_obj["cycle_nodes"] == expected_obj["cycle_nodes"], (
            f"Expected cycle_nodes {expected_obj['cycle_nodes']} at index {i}, "
            f"but got {actual_obj['cycle_nodes']}."
        )

        assert actual_obj["researchers"] == expected_obj["researchers"], (
            f"Expected researchers {expected_obj['researchers']} at index {i}, "
            f"but got {actual_obj['researchers']}."
        )