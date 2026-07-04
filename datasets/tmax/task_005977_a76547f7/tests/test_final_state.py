# test_final_state.py

import os
import sqlite3
import pytest

def test_graph_db_exists_and_valid():
    """Check if graph.db exists and contains the required tables and data."""
    db_path = "/home/user/data/graph.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    # Connect to the database and check tables
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if nodes table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='nodes';")
        assert cursor.fetchone() is not None, "Table 'nodes' is missing in graph.db."

        # Check if edges table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='edges';")
        assert cursor.fetchone() is not None, "Table 'edges' is missing in graph.db."

        # Check if data was inserted
        cursor.execute("SELECT COUNT(*) FROM nodes;")
        nodes_count = cursor.fetchone()[0]
        assert nodes_count > 0, "Table 'nodes' is empty."

        cursor.execute("SELECT COUNT(*) FROM edges;")
        edges_count = cursor.fetchone()[0]
        assert edges_count > 0, "Table 'edges' is empty."

    except sqlite3.Error as e:
        pytest.fail(f"Failed to read SQLite database {db_path}: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def test_top_department_result():
    """Check if top_department.txt exists and contains the correct result."""
    result_path = "/home/user/data/top_department.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} is missing."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected_content = "Engineering,0.75"
    assert content == expected_content, f"Expected '{expected_content}', but found '{content}' in {result_path}."