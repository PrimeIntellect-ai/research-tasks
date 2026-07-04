# test_final_state.py

import os
import json
import pytest

def test_c_program_exists():
    assert os.path.isfile("/home/user/shortest_path.c"), "/home/user/shortest_path.c is missing"

def test_bash_script_exists():
    assert os.path.isfile("/home/user/pipeline.sh"), "/home/user/pipeline.sh is missing"

def test_json_output_exists_and_valid():
    output_path = "/home/user/path_output.json"
    assert os.path.isfile(output_path), f"{output_path} is missing. Did you run pipeline.sh 1 7?"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} does not contain valid JSON.")

    assert "path" in data, "'path' key missing in JSON output"
    assert "length" in data, "'length' key missing in JSON output"

    assert data["length"] == 3, f"Expected length 3, got {data['length']}"

    expected_path = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"},
        {"id": 7, "name": "Grace"}
    ]

    # The IDs in the JSON might be strings or ints depending on how the script generated it, 
    # but the prompt schema shows integers. Let's handle both gracefully or enforce schema.
    # The schema requires ints.

    actual_path = data["path"]
    assert len(actual_path) == 4, f"Expected path of length 4 nodes, got {len(actual_path)}"

    for i, expected_node in enumerate(expected_path):
        assert int(actual_path[i]["id"]) == expected_node["id"], f"Expected node id {expected_node['id']} at position {i}"
        assert actual_path[i]["name"] == expected_node["name"], f"Expected node name {expected_node['name']} at position {i}"