# test_final_state.py
import json
import sqlite3
import os
import pytest

DB_PATH = '/home/user/graph_data/knowledge.db'
JSON_PATH = '/home/user/graph_data/downstream_nodes.json'

def test_unique_index_created():
    assert os.path.exists(DB_PATH), f"Database missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_unique_edges'")
    idx = cur.fetchone()
    conn.close()
    assert idx is not None, "Unique index 'idx_unique_edges' was not created on the edges table."

def test_edges_table_state():
    assert os.path.exists(DB_PATH), f"Database missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check total rows
    cur.execute("SELECT count(*) FROM edges")
    count = cur.fetchone()[0]
    assert count == 7, f"Expected exactly 7 edges after cleaning and upserting, but found {count}."

    # Check if duplicates are removed
    cur.execute("SELECT source, target, COUNT(*) FROM edges GROUP BY source, target HAVING COUNT(*) > 1")
    duplicates = cur.fetchall()
    assert len(duplicates) == 0, "Stale rows were not properly deleted. Duplicate (source, target) pairs still exist."

    # Check specific updates
    cur.execute("SELECT weight, updated_at FROM edges WHERE source='ROOT_42' AND target='N_2'")
    res = cur.fetchone()
    assert res is not None, "Edge ROOT_42 -> N_2 is missing."
    assert res[0] == 3.0 and res[1] == 200, f"Edge ROOT_42 -> N_2 was not updated correctly. Expected weight 3.0, updated_at 200, got {res}."

    # Check ignored stale update
    cur.execute("SELECT weight, updated_at FROM edges WHERE source='N_1' AND target='N_3'")
    res = cur.fetchone()
    assert res is not None, "Edge N_1 -> N_3 is missing."
    assert res[0] == 2.0 and res[1] == 150, f"Edge N_1 -> N_3 was incorrectly updated with stale data. Expected weight 2.0, updated_at 150, got {res}."

    # Check new edge
    cur.execute("SELECT weight, updated_at FROM edges WHERE source='N_4' AND target='N_6'")
    res = cur.fetchone()
    assert res is not None, "New edge N_4 -> N_6 from CSV was not inserted."
    assert res[0] == 1.0 and res[1] == 300, f"New edge N_4 -> N_6 has incorrect data. Expected weight 1.0, updated_at 300, got {res}."

    conn.close()

def test_json_output():
    assert os.path.exists(JSON_PATH), f"JSON output file missing at {JSON_PATH}"

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file downstream_nodes.json is not a valid JSON.")

    expected = {
        "N_1": 1,
        "N_2": 1,
        "N_3": 2,
        "N_5": 2,
        "N_4": 3,
        "ROOT_42": 3,
        "N_6": 4
    }

    assert isinstance(data, dict), "JSON root should be a dictionary."

    for node, hops in expected.items():
        assert node in data, f"Node {node} is missing from the output JSON."
        assert data[node] == hops, f"Incorrect hop count for {node}. Expected {hops}, got {data[node]}."

    for node in data:
        assert node in expected, f"Unexpected node {node} found in the output JSON."