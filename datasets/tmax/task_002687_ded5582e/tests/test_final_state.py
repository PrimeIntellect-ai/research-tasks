# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_files_exist():
    """Verify that the required script and source files exist."""
    required_files = [
        "/home/user/query.sql",
        "/home/user/build_graph.go",
        "/home/user/run_etl.sh",
        "/home/user/graph_projection.json"
    ]
    for file_path in required_files:
        assert os.path.isfile(file_path), f"Required file {file_path} is missing."

def test_json_output():
    """Verify that the generated JSON output is correct based on the database state."""
    json_path = "/home/user/graph_projection.json"
    db_path = "/home/user/system.db"

    assert os.path.isfile(json_path), f"{json_path} does not exist."
    assert os.path.isfile(db_path), f"{db_path} does not exist."

    # Compute expected result directly from the database to ensure correctness
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT DISTINCT s1.name as source, s3.name as target
    FROM dependencies d1
    JOIN dependencies d2 ON d1.depends_on_id = d2.service_id
    JOIN services s1 ON d1.service_id = s1.id
    JOIN services s3 ON d2.depends_on_id = s3.id
    WHERE NOT EXISTS (
        SELECT 1 FROM dependencies d3 
        WHERE d3.service_id = d1.service_id AND d3.depends_on_id = d2.depends_on_id
    )
    ORDER BY source, target;
    """

    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_json = [{"source": row[0], "target": row[1]} for row in expected_rows]

    with open(json_path, 'r') as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert isinstance(actual_json, list), "JSON output must be a list of objects."

    # Sort both just in case, though the task requires sorting
    actual_sorted = sorted(actual_json, key=lambda x: (x.get("source", ""), x.get("target", "")))
    expected_sorted = sorted(expected_json, key=lambda x: (x["source"], x["target"]))

    assert actual_sorted == expected_sorted, f"JSON output does not match expected hidden 2-hop dependencies. Expected: {expected_sorted}, Got: {actual_sorted}"

def test_json_structure_and_sorting():
    """Verify the JSON file is structurally correct and sorted as requested."""
    json_path = "/home/user/graph_projection.json"

    with open(json_path, 'r') as f:
        actual_json = json.load(f)

    for item in actual_json:
        assert set(item.keys()) == {"source", "target"}, f"JSON objects must contain exactly 'source' and 'target' keys. Found: {item.keys()}"

    # Check if it was already sorted
    actual_sorted = sorted(actual_json, key=lambda x: (x.get("source", ""), x.get("target", "")))
    assert actual_json == actual_sorted, "The JSON array is not sorted alphabetically by source, then target."