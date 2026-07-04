# test_final_state.py
import os
import sqlite3
import pytest

DB_PATH = "/home/user/graph.db"
QUERY_PLAN_PATH = "/home/user/query_plan.txt"
MAX_TRIANGLE_PATH = "/home/user/max_triangle.txt"
EXECUTABLE_PATH = "/home/user/triangle_analyzer"

def test_idx_stale_removed():
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} missing."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_stale';")
    result = c.fetchone()
    conn.close()
    assert result is None, "The stale index 'idx_stale' was not removed."

def test_new_index_created():
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} missing."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges';")
    indexes = c.fetchall()
    conn.close()
    assert len(indexes) > 0, "No indexes found on the 'edges' table. An optimal index should have been created."
    # Also ensure the index actually helps the query (optional, but checking existence is a good start)

def test_query_plan_output():
    assert os.path.exists(QUERY_PLAN_PATH), f"Query plan output {QUERY_PLAN_PATH} is missing."
    with open(QUERY_PLAN_PATH, "r") as f:
        content = f.read().upper()

    assert "SEARCH" in content, "Query plan does not indicate index usage (missing 'SEARCH')."
    assert "SCAN TABLE EDGES" not in content, "Query plan indicates full table scan on 'edges' (found 'SCAN TABLE edges')."

def test_max_triangle_output():
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} missing."

    # Dynamically compute the expected answer
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT e1.src, COUNT(*) as triangles 
        FROM edges e1 
        JOIN edges e2 ON e1.dst = e2.src 
        JOIN edges e3 ON e2.dst = e3.src 
        WHERE e3.dst = e1.src 
        GROUP BY e1.src 
        ORDER BY triangles DESC 
        LIMIT 1;
    ''')
    result = c.fetchone()
    conn.close()

    assert result is not None, "Database has no triangles."
    expected_output = f"{result[0]},{result[1]}"

    assert os.path.exists(MAX_TRIANGLE_PATH), f"Max triangle output {MAX_TRIANGLE_PATH} is missing."
    with open(MAX_TRIANGLE_PATH, "r") as f:
        content = f.read().strip()

    assert content == expected_output, f"Expected output '{expected_output}', but got '{content}'."

def test_executable_exists():
    assert os.path.exists(EXECUTABLE_PATH), f"Executable {EXECUTABLE_PATH} is missing."
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"File {EXECUTABLE_PATH} is not executable."