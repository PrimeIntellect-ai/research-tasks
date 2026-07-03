# test_final_state.py
import os
import json
import pytest

def test_go_file_exists():
    go_file = "/home/user/find_deadlocks.go"
    assert os.path.isfile(go_file), f"Go source file {go_file} does not exist."

def test_json_output_exists():
    json_file = "/home/user/deadlocks.json"
    assert os.path.isfile(json_file), f"JSON output file {json_file} does not exist."

def test_json_output_content():
    json_file = "/home/user/deadlocks.json"
    assert os.path.isfile(json_file), f"JSON output file {json_file} does not exist."

    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_file} does not contain valid JSON.")

    assert "deadlocks" in data, "JSON output is missing the 'deadlocks' key."

    deadlocks = data["deadlocks"]
    assert isinstance(deadlocks, list), "'deadlocks' should be a list."

    # Normalize the cycles just in case the student's sort order is slightly off,
    # but the instructions say "Represent each unique cycle starting with the transaction that comes first alphabetically. Sorts the list of cycles alphabetically..."

    expected_deadlocks = [
        ["T_A", "T_B", "T_C"],
        ["T_D", "T_E"],
        ["T_W", "T_X", "T_Y", "T_Z"]
    ]

    assert deadlocks == expected_deadlocks, f"Expected deadlocks {expected_deadlocks}, but got {deadlocks}."