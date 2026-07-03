# test_final_state.py

import os
import json
import pytest

def test_c_program_exists():
    """Verify that the C program was created."""
    c_file = "/home/user/analyze_graph.c"
    assert os.path.isfile(c_file), f"The C program {c_file} does not exist."

def test_json_output_exists():
    """Verify that the JSON output file was created."""
    json_file = "/home/user/index_priority.json"
    assert os.path.isfile(json_file), f"The JSON output file {json_file} does not exist."

def test_json_output_content():
    """Verify that the JSON output contains the correct top 3 nodes."""
    json_file = "/home/user/index_priority.json"

    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_file} does not contain valid JSON.")

    expected = [
        {"node_id": 3, "degree": 6},
        {"node_id": 6, "degree": 6},
        {"node_id": 1, "degree": 5}
    ]

    assert isinstance(data, list), "The JSON output must be a list of objects."
    assert len(data) == 3, f"Expected exactly 3 items in the JSON array, got {len(data)}."

    for i in range(3):
        assert data[i] == expected[i], f"Mismatch at index {i}. Expected {expected[i]}, got {data[i]}."