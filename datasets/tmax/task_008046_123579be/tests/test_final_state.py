# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = '/home/user/graph.db'
JSON_PATH = '/home/user/subgraph.json'

def test_index_exists():
    """Check if the index idx_edges_source was created on the edges table."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_edges_source'")
        index_row = c.fetchone()
        assert index_row is not None, "Index 'idx_edges_source' is missing in the database."
    except sqlite3.Error as e:
        pytest.fail(f"SQLite error occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def test_json_exists_and_content():
    """Check if the exported JSON file exists and contains the correct traversal results."""
    assert os.path.exists(JSON_PATH), f"Exported JSON file {JSON_PATH} is missing."

    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON from {JSON_PATH}: {e}")
    except Exception as e:
        pytest.fail(f"Error reading {JSON_PATH}: {e}")

    expected_data = [
        {
            "source_id": 42,
            "target_id": 101,
            "target_name": "child1",
            "target_category": "sub",
            "depth": 1
        },
        {
            "source_id": 42,
            "target_id": 102,
            "target_name": "child2",
            "target_category": "sub",
            "depth": 1
        },
        {
            "source_id": 101,
            "target_id": 201,
            "target_name": "grandchild1",
            "target_category": "leaf",
            "depth": 2
        },
        {
            "source_id": 102,
            "target_id": 202,
            "target_name": "grandchild2",
            "target_category": "leaf",
            "depth": 2
        },
        {
            "source_id": 202,
            "target_id": 301,
            "target_name": "greatgrandchild1",
            "target_category": "leaf",
            "depth": 3
        }
    ]

    assert isinstance(data, list), "JSON root must be an array."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual == expected, f"Mismatch at index {i}. Expected {expected}, got {actual}."