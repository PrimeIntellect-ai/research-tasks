# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/backups.db"
C_FILE_PATH = "/home/user/recovery.c"
OUTPUT_PATH = "/home/user/recovery_path.txt"

def test_database_optimization():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check that the bad index was dropped
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_edges_bad';")
    assert cursor.fetchone() is None, "The inefficient index 'idx_edges_bad' was not dropped."

    # Check that the new covering index was created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_edges_cov';")
    assert cursor.fetchone() is not None, "The covering index 'idx_edges_cov' was not created."

    # Check the columns of the new index to ensure it is covering and correctly ordered
    cursor.execute("PRAGMA index_info('idx_edges_cov');")
    columns = [row[2] for row in cursor.fetchall()]
    expected_columns = ['source', 'target', 'weight']
    assert columns == expected_columns, f"The index 'idx_edges_cov' does not have the correct columns or order. Expected {expected_columns}, got {columns}."

    conn.close()

def test_c_code_implemented():
    assert os.path.isfile(C_FILE_PATH), f"C source file {C_FILE_PATH} is missing."

    with open(C_FILE_PATH, "r") as f:
        content = f.read()

    assert "sqlite3_prepare" in content, "The C file does not use 'sqlite3_prepare' or 'sqlite3_prepare_v2'."
    assert "sqlite3_bind_text" in content, "The C file does not use 'sqlite3_bind_text' for parameterized queries."
    assert "sprintf" not in content.split("process_neighbors")[1], "The C file should not use sprintf inside the query building logic."

def test_recovery_path_output():
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing."

    with open(OUTPUT_PATH, "r") as f:
        content = f.read().strip()

    expected_path = "Start->B->A->C->Recovery"
    assert content == expected_path, f"The calculated recovery path is incorrect. Expected '{expected_path}', got '{content}'."