# test_final_state.py

import os
import json
import pytest

def test_output_file_exists_and_valid():
    output_path = "/home/user/output/path.json"
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    with open(output_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_path} does not contain valid JSON.")

    assert "path" in data, "The JSON output must contain a 'path' key."

    path_data = data["path"]
    assert isinstance(path_data, list), "The 'path' key must map to a JSON array."

    expected_path = [
        {"id": 1, "name": "Alice", "topics": ["AI", "Graph"]},
        {"id": 4, "name": "Diana", "topics": ["Data Science", "AI"]},
        {"id": 5, "name": "Eve", "topics": ["Graph", "Bioinformatics"]}
    ]

    assert len(path_data) == len(expected_path), f"Expected path length of {len(expected_path)}, but got {len(path_data)}."

    for i, (actual_node, expected_node) in enumerate(zip(path_data, expected_path)):
        assert "id" in actual_node, f"Node at index {i} is missing the 'id' field."
        assert "name" in actual_node, f"Node at index {i} is missing the 'name' field."
        assert "topics" in actual_node, f"Node at index {i} is missing the 'topics' field."

        assert actual_node["id"] == expected_node["id"], f"Node at index {i} has incorrect 'id'. Expected {expected_node['id']}, got {actual_node['id']}."
        assert actual_node["name"] == expected_node["name"], f"Node at index {i} has incorrect 'name'. Expected {expected_node['name']}, got {actual_node['name']}."

        # Sort topics in case the student program changes the order, though it should ideally match exactly.
        actual_topics = sorted(actual_node["topics"]) if isinstance(actual_node["topics"], list) else actual_node["topics"]
        expected_topics = sorted(expected_node["topics"])
        assert actual_topics == expected_topics, f"Node at index {i} has incorrect 'topics'. Expected {expected_topics}, got {actual_topics}."