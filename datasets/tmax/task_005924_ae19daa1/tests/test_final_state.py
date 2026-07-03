# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/graph_tool/graph.db"
OUTPUT_PATH = "/home/user/graph_tool/output.json"

def test_database_index_created():
    """Verify that an index on the 'source' column of the 'edges' table was created."""
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} not found."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all indexes on the 'edges' table
    cursor.execute("PRAGMA index_list('edges');")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No index found on the 'edges' table."

    # Check if any index covers the 'source' column
    has_source_index = False
    for idx in indexes:
        idx_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{idx_name}');")
        columns = cursor.fetchall()
        # columns format: (seqno, cid, name)
        if any(col[2] == 'source' for col in columns):
            has_source_index = True
            break

    assert has_source_index, "No index found covering the 'source' column of the 'edges' table."
    conn.close()

def test_output_json_correctness():
    """Verify that the output.json file exists and contains the correct shortest path."""
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} not found."

    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} does not contain valid JSON.")

    assert "path" in data, "'path' key is missing in the JSON output."
    assert "hops" in data, "'hops' key is missing in the JSON output."

    expected_path = ["START", "M", "END"]
    expected_hops = 2

    assert data["path"] == expected_path, f"Incorrect shortest path. Expected {expected_path}, got {data['path']}."
    assert data["hops"] == expected_hops, f"Incorrect hops count. Expected {expected_hops}, got {data['hops']}."

def test_database_data_unmodified():
    """Verify that the original data in the 'edges' table was not modified."""
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} not found."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM edges;")
    count = cursor.fetchone()[0]
    assert count == 10, f"Expected 10 rows in the 'edges' table, but found {count}. The data was modified."

    conn.close()