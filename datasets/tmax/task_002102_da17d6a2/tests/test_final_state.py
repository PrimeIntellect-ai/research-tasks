# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/source.db"
JSON_PATH = "/home/user/active_graph.json"

def test_database_indices_fixed():
    assert os.path.isfile(DB_PATH), f"Database file not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check that corrupt index is dropped
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_corrupt_source';")
    assert cursor.fetchone() is None, "The index 'idx_corrupt_source' was not dropped from the database."

    # Check that new optimized index is created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_events_optimized';")
    assert cursor.fetchone() is not None, "The index 'idx_events_optimized' was not created in the database."

    conn.close()

def test_active_graph_json_output():
    assert os.path.isfile(JSON_PATH), f"Output JSON file not found at {JSON_PATH}"

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {JSON_PATH} does not contain valid JSON.")

    # The expected active graph based on the seed data
    expected_data = {
        "1": [2],
        "2": [4, 5]
    }

    assert data == expected_data, f"The content of {JSON_PATH} does not match the expected final graph state. Expected: {expected_data}, Got: {data}"