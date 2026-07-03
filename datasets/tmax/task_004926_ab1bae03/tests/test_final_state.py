# test_final_state.py

import os
import sqlite3
import pytest

def test_libmath_so_exists():
    path = "/home/user/libmath.so"
    assert os.path.isfile(path), f"Shared library {path} does not exist. Did you compile math_lib.c?"
    assert os.access(path, os.R_OK), f"Cannot read {path}."

def test_sqlite_db_schema_migrated():
    path = "/home/user/data.db"
    assert os.path.isfile(path), f"Database file {path} does not exist."

    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(records);")
    columns = {row[1]: row[2] for row in cursor.fetchall()}

    assert "variance" in columns, "Column 'variance' missing from 'records' table. Schema migration failed."
    assert "REAL" in columns["variance"].upper(), "Column 'variance' should be of type REAL."

    conn.close()

def test_sqlite_db_data_inserted():
    path = "/home/user/data.db"
    assert os.path.isfile(path), f"Database file {path} does not exist."

    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute("SELECT input_mean, variance FROM records WHERE input_mean = 30.0;")
    rows = cursor.fetchall()

    assert len(rows) > 0, "No record found with input_mean = 30.0. Did the script insert the processed data?"

    # Check if any row has the correct variance (200.0)
    found_correct_variance = any(abs(row[1] - 200.0) < 0.001 for row in rows if row[1] is not None)
    assert found_correct_variance, "Record with input_mean = 30.0 found, but variance is not 200.0."

    conn.close()

def test_error_log_exists_and_correct():
    path = "/home/user/error.log"
    assert os.path.isfile(path), f"Error log file {path} does not exist. Did the script handle invalid input correctly?"

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "INVALID_INPUT", f"Error log content is incorrect. Expected 'INVALID_INPUT', got '{content}'."

def test_process_py_exists():
    path = "/home/user/process.py"
    assert os.path.isfile(path), f"Python script {path} does not exist."