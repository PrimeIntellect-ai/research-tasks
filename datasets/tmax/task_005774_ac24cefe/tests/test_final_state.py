# test_final_state.py
import os
import json
import pytest

JSON_PATH = "/home/user/lineage_export.json"
GO_FILE_PATH = "/home/user/export_lineage.go"

def test_go_file_exists():
    assert os.path.exists(GO_FILE_PATH), f"Go source file {GO_FILE_PATH} does not exist."
    assert os.path.isfile(GO_FILE_PATH), f"{GO_FILE_PATH} is not a file."

def test_json_export_exists():
    assert os.path.exists(JSON_PATH), f"JSON export file {JSON_PATH} does not exist."
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a file."

def test_json_export_content():
    try:
        with open(JSON_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON from {JSON_PATH}: {e}")

    assert "nodes" in data, "JSON output is missing the 'nodes' key."
    assert "edges" in data, "JSON output is missing the 'edges' key."

    # Validate nodes
    expected_node_ids = {1, 2, 3, 4, 7}
    actual_nodes = data["nodes"]

    # Check that each node has required keys
    for node in actual_nodes:
        assert "id" in node, f"Node missing 'id': {node}"
        assert "title" in node, f"Node missing 'title': {node}"
        assert "format" in node, f"Node missing 'format': {node}"

    actual_node_ids = {n["id"] for n in actual_nodes}
    assert actual_node_ids == expected_node_ids, f"Node ID mismatch. Expected {expected_node_ids}, got {actual_node_ids}"

    # Validate edges
    expected_edges = {
        (1, 2, 'clean'),
        (2, 3, 'aggregate'),
        (3, 4, 'detect_anomalies'),
        (3, 7, 'join')
    }
    actual_edges_list = data["edges"]

    # Check that each edge has required keys
    for edge in actual_edges_list:
        assert "source" in edge, f"Edge missing 'source': {edge}"
        assert "target" in edge, f"Edge missing 'target': {edge}"
        assert "operation" in edge, f"Edge missing 'operation': {edge}"

    actual_edges = {(e["source"], e["target"], e["operation"]) for e in actual_edges_list}
    assert actual_edges == expected_edges, f"Edge mismatch. Expected {expected_edges}, got {actual_edges}"