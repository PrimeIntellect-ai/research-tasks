# test_final_state.py

import os
import sqlite3
import json
import pytest

def test_indexes_created():
    db_path = "/home/user/citations.db"
    assert os.path.exists(db_path), f"Database file missing: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='citations';")
    indexes = cursor.fetchall()

    assert len(indexes) > 0, "No indexes found on 'citations' table. You need to create optimal indexes for graph traversal."

    conn.close()

def test_shortest_path_json():
    json_path = "/home/user/shortest_path.json"
    assert os.path.exists(json_path), f"JSON file missing: {json_path}"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "path_length" in data, "Missing 'path_length' key in JSON."
    assert "path" in data, "Missing 'path' key in JSON."

    assert data["path_length"] == 2, f"Expected path_length to be 2, got {data['path_length']}."

    expected_path = [
        {"id": "P1", "title": "Deep Learning"},
        {"id": "P4", "title": "Optimization Methods"},
        {"id": "P5", "title": "Adam Optimizer"}
    ]

    assert data["path"] == expected_path, f"Expected path {expected_path}, got {data['path']}."