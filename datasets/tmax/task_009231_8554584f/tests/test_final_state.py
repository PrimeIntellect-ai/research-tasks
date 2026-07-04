# test_final_state.py

import os
import json
import pytest

def test_go_file_exists():
    """Test that the Go program exists."""
    file_path = "/home/user/analytics/build_graph.go"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

def test_database_exists():
    """Test that the SQLite database file exists."""
    file_path = "/home/user/analytics/graph.db"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

def test_output_json_exists_and_content():
    """Test that output.json exists, is valid JSON, and has the correct structure."""
    file_path = "/home/user/analytics/output.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    expected_data = [
        {
            "source_node": "A",
            "total_interactions": 11,
            "connections": [
                {"target_node": "B", "weight": 5},
                {"target_node": "C", "weight": 6}
            ]
        },
        {
            "source_node": "D",
            "total_interactions": 16,
            "connections": [
                {"target_node": "A", "weight": 15},
                {"target_node": "B", "weight": 1}
            ]
        },
        {
            "source_node": "G",
            "total_interactions": 12,
            "connections": [
                {"target_node": "H", "weight": 12}
            ]
        },
        {
            "source_node": "H",
            "total_interactions": 20,
            "connections": [
                {"target_node": "A", "weight": 10},
                {"target_node": "B", "weight": 10}
            ]
        }
    ]

    assert data == expected_data, "The contents of output.json do not match the expected graph projection."