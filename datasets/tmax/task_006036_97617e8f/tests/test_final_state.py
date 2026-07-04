# test_final_state.py
import os
import sqlite3
import pytest

def test_build_and_run_script_exists():
    script_path = "/home/user/pipeline/build_and_run.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_database_exists():
    db_path = "/home/user/pipeline/results.db"
    assert os.path.isfile(db_path), f"The database {db_path} does not exist."

def test_database_contents():
    db_path = "/home/user/pipeline/results.db"
    assert os.path.isfile(db_path), f"The database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table 'projections' exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projections';")
    table_exists = cursor.fetchone()
    assert table_exists is not None, "Table 'projections' does not exist in the database."

    # Query the results
    cursor.execute("""
        SELECT record_id, ROUND(p1, 4), ROUND(p2, 4), ROUND(p3, 4) 
        FROM projections 
        ORDER BY record_id;
    """)
    rows = cursor.fetchall()
    conn.close()

    expected_rows = [
        ("rec_001", -0.1983, -1.4967, 1.9365),
        ("rec_002", -0.5358, 0.9022, 0.8413),
        ("rec_004", 0.1983, 1.4967, -1.9365),
        ("rec_005", 2.1332, 8.7618, -5.4093)
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in 'projections', but got {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
        assert actual[0] == expected[0], f"Row {i+1}: Expected record_id '{expected[0]}', got '{actual[0]}'."
        assert abs(actual[1] - expected[1]) <= 0.0001, f"Row {i+1} ({actual[0]}): Expected p1 approx {expected[1]}, got {actual[1]}."
        assert abs(actual[2] - expected[2]) <= 0.0001, f"Row {i+1} ({actual[0]}): Expected p2 approx {expected[2]}, got {actual[2]}."
        assert abs(actual[3] - expected[3]) <= 0.0001, f"Row {i+1} ({actual[0]}): Expected p3 approx {expected[3]}, got {actual[3]}."