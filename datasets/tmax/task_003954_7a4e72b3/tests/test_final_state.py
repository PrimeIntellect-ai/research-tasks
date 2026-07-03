# test_final_state.py
import os
import sqlite3
import pytest

DB_PATH = '/home/user/topology.db'
OUTPUT_FILE = '/home/user/min_latency.txt'

def get_expected_min_latency(db_path):
    """Dynamically compute the expected minimum latency for compute-only triangles."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query = """
        SELECT MIN(e1.latency + e2.latency + e3.latency)
        FROM edges e1
        JOIN edges e2 ON e1.dst = e2.src
        JOIN edges e3 ON e2.dst = e3.src AND e3.dst = e1.src
        JOIN nodes n1 ON e1.src = n1.id
        JOIN nodes n2 ON e2.src = n2.id
        JOIN nodes n3 ON e3.src = n3.id
        WHERE n1.role = 'compute' 
          AND n2.role = 'compute' 
          AND n3.role = 'compute'
    """
    c.execute(query)
    result = c.fetchone()[0]
    conn.close()
    return result

def test_database_integrity():
    """Verify that the database and necessary structures are intact."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if index exists (user was supposed to recreate it or reindex)
    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_edges_src'")
    index_exists = c.fetchone()
    conn.close()

    assert index_exists is not None, "Index 'idx_edges_src' is missing. It should have been recreated or kept intact."

def test_min_latency_output():
    """Verify that the output file contains the correct minimum latency."""
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."

    with open(OUTPUT_FILE, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"Output file should contain only an integer, got: {content}"

    actual_val = int(content)
    expected_val = get_expected_min_latency(DB_PATH)

    assert expected_val is not None, "No compute-only triangles found in the database."
    assert actual_val == expected_val, f"Incorrect minimum latency. Expected {expected_val}, got {actual_val}."