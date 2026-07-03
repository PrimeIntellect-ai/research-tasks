# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = '/home/user/graph.db'
RESULTS_PATH = '/home/user/optimized_results.json'
QUERY_PLAN_PATH = '/home/user/query_plan.txt'
SCRIPT_PATH = '/home/user/fast_pipeline.py'

def test_database_index():
    """Verify that an index was created on the Edges table for source_id."""
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA index_list('Edges')")
    indexes = c.fetchall()
    assert indexes, "No index found on the 'Edges' table."

    valid_index_found = False
    for idx in indexes:
        idx_name = idx[1]
        c.execute(f"PRAGMA index_info('{idx_name}')")
        columns = [row[2] for row in c.fetchall()]
        if columns and columns[0] == 'source_id':
            valid_index_found = True
            break

    conn.close()
    assert valid_index_found, "An index on 'Edges' starting with 'source_id' is required."

def test_optimized_results_json():
    """Verify the contents of the generated JSON file."""
    assert os.path.isfile(RESULTS_PATH), f"Expected JSON file {RESULTS_PATH} is missing."

    with open(RESULTS_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} does not contain valid JSON.")

    expected_data = {
        "S1": ["D1", "D2", "Q1", "S2"],
        "S2": ["D1", "D2", "Q1"],
        "S3": ["A1", "A2", "D2"]
    }

    assert data == expected_data, f"JSON contents do not match expected output. Got: {data}"

def test_query_plan_log():
    """Verify the query plan log exists and shows index usage."""
    assert os.path.isfile(QUERY_PLAN_PATH), f"Query plan log {QUERY_PLAN_PATH} is missing."

    with open(QUERY_PLAN_PATH, 'r') as f:
        content = f.read().lower()

    assert content.strip() != "", "Query plan log is empty."
    assert "index" in content, "Query plan does not appear to use an index (missing 'INDEX' keyword)."

def test_python_script_exists_and_recursive():
    """Verify the Python script exists and uses a Recursive CTE."""
    assert os.path.isfile(SCRIPT_PATH), f"Python script {SCRIPT_PATH} is missing."

    with open(SCRIPT_PATH, 'r') as f:
        content = f.read().lower()

    assert "with recursive" in content, "The Python script must contain a 'WITH RECURSIVE' SQL statement."