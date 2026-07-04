# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/service_backup.db'
JSON_PATH = '/home/user/graph_materialized.json'

def test_secondary_indexes_dropped():
    """Verify that all secondary indexes have been dropped from the database."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Fetch all indexes
    cur.execute("SELECT name, sql FROM sqlite_master WHERE type='index';")
    indexes = cur.fetchall()
    conn.close()

    # We expect no secondary indexes. SQLite might have auto-indexes for UNIQUE constraints
    # (like sqlite_autoindex_tbl_entity_registry_1). These have sql=None.
    # Any index created explicitly with CREATE INDEX will have a non-NULL sql.
    explicit_indexes = [name for name, sql in indexes if sql is not None]

    assert len(explicit_indexes) == 0, f"Found unexpected secondary indexes: {explicit_indexes}"

def test_json_output_exists_and_valid():
    """Verify the JSON file exists and is valid JSON."""
    assert os.path.exists(JSON_PATH), f"Output JSON file missing at {JSON_PATH}"

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"File {JSON_PATH} contains invalid JSON: {e}")

    assert isinstance(data, dict), "JSON root must be an object (dictionary)"

def test_json_output_matches_database():
    """Recompute the graph from the database and verify it matches the JSON output."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    assert os.path.exists(JSON_PATH), f"Output JSON file missing at {JSON_PATH}"

    # Recompute the expected graph
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Fetch all entities
    cur.execute("SELECT ent_id, ent_identifier FROM tbl_entity_registry")
    entities = {row[0]: row[1] for row in cur.fetchall()}

    # Fetch all links
    cur.execute("SELECT parent_ent_id, child_ent_id FROM tbl_entity_links")
    links = cur.fetchall()

    conn.close()

    expected_graph = {}
    for parent_id, child_id in links:
        parent_name = entities[parent_id]
        child_name = entities[child_id]

        if parent_name not in expected_graph:
            expected_graph[parent_name] = []
        expected_graph[parent_name].append(child_name)

    for parent in expected_graph:
        expected_graph[parent].sort()

    # Read actual JSON
    with open(JSON_PATH, 'r') as f:
        actual_graph = json.load(f)

    assert actual_graph == expected_graph, "The materialized graph does not match the expected adjacency list derived from the database."

def test_json_formatting():
    """Verify the JSON file is nicely formatted with indent=4."""
    assert os.path.exists(JSON_PATH), f"Output JSON file missing at {JSON_PATH}"

    with open(JSON_PATH, 'r') as f:
        content = f.read()

    # A simple heuristic: if it has newlines and spaces, it's likely formatted.
    # We can parse it and dump it with indent=4 and see if it closely matches.
    data = json.loads(content)
    expected_content = json.dumps(data, indent=4)

    # We check if the content has newlines and spaces for indentation
    assert "\n" in content, "JSON file does not appear to be formatted with newlines."
    assert "    " in content, "JSON file does not appear to be formatted with an indent of 4 spaces."