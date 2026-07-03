# test_final_state.py

import os
import sqlite3
import pytest

def test_c_source_exists():
    """Test that the C source code file exists."""
    assert os.path.isfile("/home/user/etl_processor.c"), "/home/user/etl_processor.c does not exist."

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    exe_path = "/home/user/etl_processor"
    assert os.path.isfile(exe_path), f"{exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_database_and_index_exist():
    """Test that the SQLite database exists and contains the required index."""
    db_path = "/home/user/analytics.db"
    assert os.path.isfile(db_path), f"{db_path} does not exist."

    # Connect to the database and check for the index
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND name='idx_performance';")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 1, "Index 'idx_performance' not found in the database."

def test_report_content():
    """Test that the report.out file contains the correct paginated results."""
    report_path = "/home/user/report.out"
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    expected_lines = [
        "User 80 spent 2901.69",
        "User 60 spent 2831.75",
        "User 70 spent 2822.40",
        "User 50 spent 2800.72",
        "User 19 spent 2742.02"
    ]

    with open(report_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {report_path} does not match expected output.\nExpected: {expected_lines}\nActual: {actual_lines}"