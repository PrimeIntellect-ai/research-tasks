# test_final_state.py

import os
import sqlite3
import pytest

def test_scripts_exist_and_executable():
    """Verify that the three bash scripts exist and are executable."""
    scripts = [
        "/home/user/init_db.sh",
        "/home/user/find_shortest_path.sh",
        "/home/user/pipeline.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_database_exists_and_populated():
    """Verify that the SQLite database exists and has the correct table and data."""
    db_path = "/home/user/network.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    # Try connecting and checking the edges table
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='edges';")
    table_exists = cursor.fetchone()
    assert table_exists is not None, "Table 'edges' does not exist in the database."

    cursor.execute("SELECT COUNT(*) FROM edges;")
    count = cursor.fetchone()[0]
    assert count > 0, "Table 'edges' is empty."

    conn.close()

def test_optimized_routes_log():
    """Verify that the optimized routes log is generated with the correct contents."""
    log_path = "/home/user/optimized_routes.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "DC1,DC4,23,DC1-DC2-DC3-DC4",
        "DC1,DC5,33,DC1-DC2-DC3-DC4-DC5",
        "DC2,DC6,30,DC2-DC3-DC4-DC5-DC6",
        "DC3,DC6,23,DC3-DC4-DC5-DC6"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in log, found {len(lines)}."

    for expected in expected_lines:
        assert expected in lines, f"Expected route '{expected}' not found in {log_path}."