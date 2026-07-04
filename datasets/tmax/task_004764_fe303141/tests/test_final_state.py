# test_final_state.py

import os
import sqlite3
import pytest

def test_index_exists():
    db_path = "/home/user/graph.db"
    assert os.path.exists(db_path), "Database file /home/user/graph.db is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND tbl_name='dependencies';")
    index_count = cursor.fetchone()[0]
    conn.close()

    assert index_count > 0, "No index created on the 'dependencies' table to speed up lookups."

def test_executable_exists():
    exe_path = "/home/user/extract_deps"
    assert os.path.exists(exe_path), "Compiled executable /home/user/extract_deps is missing. Did you compile the C code?"
    assert os.access(exe_path, os.X_OK), "The file /home/user/extract_deps is not executable."

def test_etl_output_csv():
    csv_path = "/home/user/etl_output.csv"
    assert os.path.exists(csv_path), "Output file /home/user/etl_output.csv is missing. Did you run the compiled program?"

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1,lib_beta",
        "1,lib_gamma",
        "2,lib_delta",
        "3,lib_epsilon",
        "4,lib_zeta"
    ]

    assert lines == expected_lines, f"etl_output.csv content does not match exactly. Expected {expected_lines}, but got {lines}."