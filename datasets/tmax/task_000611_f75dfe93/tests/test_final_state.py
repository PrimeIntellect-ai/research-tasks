# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = '/home/user/graph.db'
RESULT_PATH = '/home/user/result.json'

def test_database_index_created():
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check for user-created indexes on the 'edges' table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges'")
    indexes = cursor.fetchall()

    user_indexes = [idx[0] for idx in indexes if idx[0] and not idx[0].startswith('sqlite_')]

    assert len(user_indexes) >= 1, "No user-created index found on 'edges' table to optimize the query."
    conn.close()

def test_result_json_valid_and_correct():
    assert os.path.isfile(RESULT_PATH), f"Result file missing at {RESULT_PATH}"

    with open(RESULT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {RESULT_PATH} is not valid JSON.")

    assert "triangle_count" in data, "Key 'triangle_count' missing in result.json"
    assert "index_statements" in data, "Key 'index_statements' missing in result.json"

    # Compute the expected triangle count directly from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = '''
        SELECT COUNT(*) 
        FROM edges e1 
        JOIN edges e2 ON e1.target = e2.source 
        JOIN edges e3 ON e2.target = e3.source AND e3.target = e1.source
    '''
    cursor.execute(query)
    expected_count = cursor.fetchone()[0]
    conn.close()

    assert data["triangle_count"] == expected_count, f"Incorrect triangle_count. Expected {expected_count}, got {data['triangle_count']}."

    index_statements = data["index_statements"]
    assert isinstance(index_statements, list), "'index_statements' must be a list of strings."
    assert len(index_statements) >= 1, "'index_statements' list is empty. It should contain the CREATE INDEX statement(s)."
    for stmt in index_statements:
        assert isinstance(stmt, str), "All items in 'index_statements' must be strings."
        assert "CREATE INDEX" in stmt.upper(), f"Statement '{stmt}' does not look like a CREATE INDEX statement."