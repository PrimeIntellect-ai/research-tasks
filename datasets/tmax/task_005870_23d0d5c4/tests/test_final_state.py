# test_final_state.py

import os
import sqlite3
import pytest

def test_result_file():
    result_path = '/home/user/result.txt'
    assert os.path.exists(result_path), f"Expected result file at {result_path} does not exist."
    assert os.path.isfile(result_path), f"{result_path} is not a file."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content == '810', f"Expected result.txt to contain '810', but got '{content}'."

def test_database_and_tables():
    db_path = '/home/user/pipeline.db'
    assert os.path.exists(db_path), f"Expected database file at {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    assert 'nodes' in tables, "Table 'nodes' is missing from the database."
    assert 'edges' in tables, "Table 'edges' is missing from the database."

    # Check nodes data
    cursor.execute("SELECT id, name, compute_cost FROM nodes ORDER BY id")
    nodes = cursor.fetchall()
    assert len(nodes) == 8, f"Expected 8 rows in 'nodes' table, found {len(nodes)}."

    # Check edges data
    cursor.execute("SELECT source, target FROM edges")
    edges = cursor.fetchall()
    expected_edges = {
        ("JOB_001", "JOB_002"),
        ("JOB_001", "JOB_003"),
        ("JOB_002", "JOB_004"),
        ("JOB_003", "JOB_005"),
        ("JOB_004", "JOB_006"),
        ("JOB_005", "JOB_006"),
        ("JOB_007", "JOB_008")
    }
    actual_edges = set(edges)
    assert actual_edges == expected_edges, f"Expected edges {expected_edges}, but got {actual_edges}."

    conn.close()

def test_edges_index():
    db_path = '/home/user/pipeline.db'
    assert os.path.exists(db_path), f"Expected database file at {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check indexes
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='edges'")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "Expected at least one index on the 'edges' table."

    # Check if any index involves the 'source' column
    has_source_index = False
    for name, idx_sql in indexes:
        if idx_sql and 'source' in idx_sql.lower():
            has_source_index = True
            break

    assert has_source_index, "Expected an index on the 'edges' table to optimize 'source' lookups."

    conn.close()