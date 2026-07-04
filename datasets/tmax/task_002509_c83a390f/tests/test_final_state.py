# test_final_state.py
import os
import json
import pytest

def test_etl_go_exists():
    assert os.path.isfile("/home/user/etl.go"), "/home/user/etl.go does not exist. The task requires writing the Go program."

def test_output_json_exists():
    assert os.path.isfile("/home/user/output.json"), "/home/user/output.json does not exist. Did the Go program run successfully?"

def test_output_json_content():
    with open("/home/user/output.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/output.json is not a valid JSON file.")

    assert "top_nodes" in data, "The JSON must contain a 'top_nodes' key at the root level."
    top_nodes = data["top_nodes"]
    assert isinstance(top_nodes, list), "'top_nodes' must be a list."

    expected_nodes = [
        {"id": "N8", "category": "auth", "in_weight": 1000, "rank": 1},
        {"id": "N7", "category": "auth", "in_weight": 500, "rank": 2},
        {"id": "N6", "category": "backend", "in_weight": 200, "rank": 1},
        {"id": "N5", "category": "backend", "in_weight": 120, "rank": 2},
        {"id": "N3", "category": "frontend", "in_weight": 50, "rank": 1},
        {"id": "N1", "category": "frontend", "in_weight": 25, "rank": 2}
    ]

    assert len(top_nodes) == len(expected_nodes), f"Expected {len(expected_nodes)} nodes in 'top_nodes', but found {len(top_nodes)}."

    for i, expected in enumerate(expected_nodes):
        actual = top_nodes[i]
        assert actual.get("id") == expected["id"], f"Expected node id '{expected['id']}' at index {i}, got '{actual.get('id')}'."
        assert actual.get("category") == expected["category"], f"Expected category '{expected['category']}' at index {i}, got '{actual.get('category')}'."
        assert actual.get("in_weight") == expected["in_weight"], f"Expected in_weight {expected['in_weight']} at index {i}, got {actual.get('in_weight')}."
        assert actual.get("rank") == expected["rank"], f"Expected rank {expected['rank']} at index {i}, got {actual.get('rank')}."