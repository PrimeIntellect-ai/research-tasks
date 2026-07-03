# test_final_state.py

import os
import sqlite3
import pytest

def test_cpp_file_exists():
    """Check if the C++ source file was created."""
    path = "/home/user/process_backups.cpp"
    assert os.path.exists(path), f"C++ source file {path} does not exist."

def test_index_created():
    """Check if the query optimization index was created in the database."""
    db_path = "/home/user/backups.db"
    assert os.path.exists(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_parent_id';")
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Index 'idx_parent_id' was not created in the database."

def test_orphaned_size_file():
    """Check if the output file exists and contains the correct sum."""
    path = "/home/user/orphaned_size.txt"
    assert os.path.exists(path), f"Output file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "2150", f"Expected sum '2150' in {path}, but got '{content}'."