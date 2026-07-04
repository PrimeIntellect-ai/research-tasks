# test_final_state.py

import os
import sqlite3
import pytest

def test_c_source_file_exists():
    path = "/home/user/audit_graph.c"
    assert os.path.isfile(path), f"Expected C source file {path} is missing."

def test_database_exists():
    path = "/home/user/audit.db"
    assert os.path.isfile(path), f"Expected SQLite database {path} is missing."

def test_violations_log_content():
    path = "/home/user/violations.log"
    assert os.path.isfile(path), f"Expected log file {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = ["U1,S1", "U2,S2"]
    assert lines == expected, f"Content of {path} does not match the expected SoD violations. Got: {lines}, Expected: {expected}"

def test_database_indexes():
    db_path = "/home/user/audit.db"
    assert os.path.isfile(db_path), f"Database {db_path} is missing."

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check indexes on edges table
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND tbl_name='edges';")
        edges_index_count = cursor.fetchone()[0]
        assert edges_index_count > 0, "No indexes were created on the 'edges' table."

        # Check indexes on nodes table
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND tbl_name='nodes';")
        nodes_index_count = cursor.fetchone()[0]
        assert nodes_index_count > 0, "No indexes were created on the 'nodes' table."

    finally:
        conn.close()