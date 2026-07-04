# test_final_state.py

import os
import json
import pytest

def test_path_json_exists():
    """Test that the output JSON file was created."""
    file_path = "/home/user/path.json"
    assert os.path.isfile(file_path), f"Output file is missing: {file_path}"

def test_path_json_content():
    """Test that the output JSON file contains the correct shortest path and cost."""
    file_path = "/home/user/path.json"
    assert os.path.isfile(file_path), f"Output file is missing: {file_path}"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {file_path} as JSON: {e}")

    assert "cost" in data, "JSON output is missing the 'cost' key."
    assert "path" in data, "JSON output is missing the 'path' key."

    expected_cost = 4
    expected_path = [10, 20, 30, 42]

    assert data["cost"] == expected_cost, f"Expected cost to be {expected_cost}, but got {data['cost']}."
    assert data["path"] == expected_path, f"Expected path to be {expected_path}, but got {data['path']}."