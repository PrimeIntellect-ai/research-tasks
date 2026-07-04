# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/workspace/graph.db"
JSON_PATH = "/home/user/workspace/centrality_results.json"

def test_database_state():
    """
    Validates that the SQLite database exists, has the correct schema,
    and contains the expected number of records based on the mock dataset.
    """
    assert os.path.exists(DB_PATH), f"Database not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check tables exist
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in c.fetchall()}
    assert "Papers" in tables, "Table 'Papers' is missing in the database"
    assert "Citations" in tables, "Table 'Citations' is missing in the database"

    # Check Citations count
    c.execute("SELECT COUNT(*) FROM Citations")
    citations_count = c.fetchone()[0]
    assert citations_count == 7, f"Expected 7 citations in DB, found {citations_count}"

    # Check Papers count (P1, P2, P3, P4, P5 are explicitly defined, but all cited must be in network)
    # The prompt implies all nodes should be considered.
    c.execute("SELECT COUNT(*) FROM Papers")
    papers_count = c.fetchone()[0]
    # At least 5 papers should be in the Papers table
    assert papers_count >= 5, f"Expected at least 5 papers in DB, found {papers_count}"

    conn.close()

def test_json_results():
    """
    Validates that the centrality results JSON exists and strictly matches
    the required schema, values, and sorting order.
    """
    assert os.path.exists(JSON_PATH), f"Results JSON not found at {JSON_PATH}"

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file centrality_results.json is not valid JSON")

    assert "metrics" in data, "Root key 'metrics' is missing in the JSON output"
    metrics = data["metrics"]
    assert isinstance(metrics, list), "'metrics' should be a list"
    assert len(metrics) == 5, f"Expected 5 nodes in metrics, found {len(metrics)}"

    expected_results = [
        {"node": "P1", "degree_centrality": 4},
        {"node": "P3", "degree_centrality": 4},
        {"node": "P2", "degree_centrality": 2},
        {"node": "P4", "degree_centrality": 2},
        {"node": "P5", "degree_centrality": 2}
    ]

    for i, expected in enumerate(expected_results):
        actual = metrics[i]
        assert "node" in actual, f"Missing 'node' key at index {i}"
        assert "degree_centrality" in actual, f"Missing 'degree_centrality' key at index {i}"

        assert actual["node"] == expected["node"], \
            f"Expected node '{expected['node']}' at index {i}, but got '{actual['node']}'"
        assert actual["degree_centrality"] == expected["degree_centrality"], \
            f"Expected degree_centrality {expected['degree_centrality']} for node '{expected['node']}', but got {actual['degree_centrality']}"