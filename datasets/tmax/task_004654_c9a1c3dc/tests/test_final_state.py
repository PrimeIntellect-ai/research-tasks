# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_final_state():
    json_path = '/home/user/shortest_path.json'
    db_path = '/home/user/logistics.db'

    # Check if JSON file exists
    assert os.path.isfile(json_path), f"JSON output file {json_path} is missing."

    # Load JSON file
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {json_path} is not a valid JSON.")

    # Validate JSON structure and keys
    assert isinstance(data, dict), f"JSON root must be a dictionary, got {type(data)}."
    assert "path" in data, "JSON must contain the key 'path'."
    assert "total_distance" in data, "JSON must contain the key 'total_distance'."

    # Validate the shortest path and distance values
    # Based on the graph:
    # Alpha -> Delta (50), Delta -> Omega (5) = 55
    # Alpha -> Beta (10), Beta -> Gamma (20), Gamma -> Omega (30) = 60
    # Alpha -> Omega (100)
    # Beta -> Delta (5, inactive)
    expected_path = ["Alpha", "Delta", "Omega"]
    expected_distance = 55

    assert data["path"] == expected_path, f"Expected path {expected_path}, but got {data['path']}."
    assert data["total_distance"] == expected_distance, f"Expected total_distance {expected_distance}, but got {data['total_distance']}."