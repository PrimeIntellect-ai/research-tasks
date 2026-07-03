# test_final_state.py

import os
import sqlite3
import pytest

def test_files_exist():
    """Verify that all required files have been created."""
    expected_files = [
        '/home/user/graph_diag.cpp',
        '/home/user/graph_diag',
        '/home/user/graph.db',
        '/home/user/traversal.log',
        '/home/user/deadlock.log'
    ]
    for filepath in expected_files:
        assert os.path.isfile(filepath), f"Expected file {filepath} does not exist."

def test_database_index():
    """Verify that the required index was created in the SQLite database."""
    db_path = '/home/user/graph.db'
    assert os.path.exists(db_path), f"Database file {db_path} not found."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND name='idx_graph_traversal';")
    row = cursor.fetchone()
    conn.close()

    assert row is not None, "Index 'idx_graph_traversal' does not exist in the database."

    # Check if the index is on the edges table
    sql = row[1].lower() if row[1] else ""
    assert "edges" in sql, "Index 'idx_graph_traversal' does not seem to be on the 'edges' table."

def test_traversal_log():
    """Verify that traversal.log contains the correct reachable nodes (B, C, D)."""
    log_path = '/home/user/traversal.log'
    assert os.path.exists(log_path), f"Log file {log_path} not found."

    with open(log_path, 'r') as f:
        content = f.read().splitlines()

    # Clean up whitespace/empty lines
    nodes = {line.strip() for line in content if line.strip()}

    assert 'B' in nodes, "'B' is missing from traversal.log"
    assert 'C' in nodes, "'C' is missing from traversal.log"
    assert 'D' in nodes, "'D' is missing from traversal.log"
    # A might or might not be there depending on how the query was written, but B, C, D must be.

def test_deadlock_log():
    """Verify that deadlock.log contains the DEADLOCK_DETECTED string."""
    log_path = '/home/user/deadlock.log'
    assert os.path.exists(log_path), f"Log file {log_path} not found."

    with open(log_path, 'r') as f:
        content = f.read()

    assert 'DEADLOCK_DETECTED' in content, "The string 'DEADLOCK_DETECTED' was not found in deadlock.log"

def test_sqlite3_bind_used():
    """Verify that parameterization was used in the C++ source code."""
    cpp_path = '/home/user/graph_diag.cpp'
    assert os.path.exists(cpp_path), f"Source file {cpp_path} not found."

    with open(cpp_path, 'r') as f:
        content = f.read()

    assert 'sqlite3_bind' in content, "The source code does not appear to use 'sqlite3_bind' for parameterization."