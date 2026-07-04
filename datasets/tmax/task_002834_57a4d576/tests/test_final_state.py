# test_final_state.py
import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/backup.db"
SQL_PATH = "/home/user/index.sql"
JSONL_PATH = "/home/user/users_graph.jsonl"

def test_index_exists_and_covers_columns():
    """Test that the index idx_edges_extract exists and covers the required columns."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if index exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_edges_extract';")
    row = cursor.fetchone()
    assert row is not None, "Index 'idx_edges_extract' was not found in the database."

    # Check covered columns
    cursor.execute("PRAGMA index_info('idx_edges_extract');")
    index_info = cursor.fetchall()
    conn.close()

    assert index_info, "Index 'idx_edges_extract' has no columns."

    # The 3rd element in the pragma tuple is the column name
    indexed_columns = {info[2] for info in index_info}
    expected_columns = {"rel_type", "deleted", "source", "target"}

    missing_cols = expected_columns - indexed_columns
    assert not missing_cols, f"Index 'idx_edges_extract' is missing columns: {missing_cols}"

    # Ensure no extra columns were added unnecessarily (though order doesn't matter)
    assert indexed_columns == expected_columns, f"Index 'idx_edges_extract' contains unexpected columns: {indexed_columns - expected_columns}"

def test_sql_file_contents():
    """Test that the index.sql file contains a valid CREATE INDEX statement with required columns."""
    assert os.path.exists(SQL_PATH), f"SQL file {SQL_PATH} is missing."

    with open(SQL_PATH, "r") as f:
        content = f.read().lower()

    assert "create " in content and "index " in content, "The file must contain a CREATE INDEX statement."
    assert "idx_edges_extract" in content, "The SQL statement must name the index 'idx_edges_extract'."
    assert "edges" in content, "The SQL statement must create the index on the 'edges' table."

    expected_columns = ["rel_type", "deleted", "source", "target"]
    for col in expected_columns:
        assert col in content, f"The SQL statement is missing the column '{col}'."

def get_expected_graph():
    """Helper to derive the expected graph projection directly from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.name, g.name
        FROM nodes u
        JOIN edges e ON u.id = e.source
        JOIN nodes g ON e.target = g.id
        WHERE u.type = 'user' 
          AND g.type = 'group' 
          AND e.rel_type = 'member_of' 
          AND e.deleted = 0
    """)
    rows = cursor.fetchall()
    conn.close()

    user_groups = {}
    for user, group in rows:
        user_groups.setdefault(user, []).append(group)

    expected = []
    for user in sorted(user_groups.keys()):
        groups = sorted(user_groups[user])
        expected.append({
            "username": user,
            "centrality": len(groups),
            "groups": groups
        })
    return expected

def test_jsonl_output():
    """Test that the materialized JSONL graph matches the expected output exactly."""
    assert os.path.exists(JSONL_PATH), f"JSONL file {JSONL_PATH} is missing."

    expected_data = get_expected_graph()

    with open(JSONL_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    actual_data = []
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
            actual_data.append(obj)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {JSONL_PATH} is not valid JSON: {line}")

    # Check length
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} lines in JSONL, found {len(actual_data)}."

    # Check exact match and ordering
    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual.get("username") == expected["username"], f"Line {i+1} username mismatch or out of alphabetical order."
        assert actual.get("centrality") == expected["centrality"], f"Line {i+1} centrality mismatch for user {expected['username']}."
        assert actual.get("groups") == expected["groups"], f"Line {i+1} groups mismatch or not sorted alphabetically for user {expected['username']}."

    assert actual_data == expected_data, "The JSONL output does not exactly match the expected graph projection."