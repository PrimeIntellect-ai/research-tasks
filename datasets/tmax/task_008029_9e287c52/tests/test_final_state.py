# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_reachable_json_exists():
    """Verify that the reachable.json file was created."""
    assert os.path.isfile('/home/user/reachable.json'), "/home/user/reachable.json does not exist."

def test_reachable_json_content():
    """Verify that the reachable.json file contains the correct reachable nodes."""
    try:
        with open('/home/user/reachable.json', 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail("/home/user/reachable.json does not contain valid JSON.")

    expected = [42, 100, 101, 200, 201, 202, 300, 301]

    assert isinstance(data, list), "The JSON output must be a list."
    assert data == expected, f"Expected {expected}, but got {data}. Check your recursive CTE and depth constraint."

def test_edges_index_created():
    """Verify that an index was created on the edges table."""
    db_path = '/home/user/graph.db'
    assert os.path.isfile(db_path), f"{db_path} is missing."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges';")
    indexes = c.fetchall()
    conn.close()

    assert len(indexes) > 0, "No index was created on the 'edges' table."