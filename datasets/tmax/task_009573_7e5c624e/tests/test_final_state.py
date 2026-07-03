# test_final_state.py

import os
import json
import pytest

def test_process_graph_cpp_exists():
    cpp_file = "/home/user/process_graph.cpp"
    assert os.path.isfile(cpp_file), f"The C++ source file {cpp_file} does not exist."

def test_top_authors_json_exists_and_valid():
    json_file = "/home/user/top_authors.json"
    assert os.path.isfile(json_file), f"The output file {json_file} does not exist."

    with open(json_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON from {json_file}: {e}")

    assert isinstance(data, list), "The JSON root should be a list."
    assert len(data) == 3, f"Expected exactly 3 authors in the JSON, but found {len(data)}."

    expected_data = [
        {"author_id": 1, "name": "Alice", "centrality": 6},
        {"author_id": 2, "name": "Bob", "centrality": 3},
        {"author_id": 3, "name": "Charlie", "centrality": 3}
    ]

    for i, expected in enumerate(expected_data):
        assert data[i] == expected, f"Mismatch at index {i}. Expected {expected}, got {data[i]}."