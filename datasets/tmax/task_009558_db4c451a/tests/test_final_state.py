# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/graph.db"
CSV_PATH = "/home/user/triangles.csv"

def test_bad_idx_dropped():
    """Test that 'bad_idx' index has been dropped."""
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='bad_idx';")
    result = cursor.fetchone()
    conn.close()
    assert result is None, "Index 'bad_idx' still exists in the database. It should have been dropped."

def test_good_idx_created():
    """Test that 'good_idx' index has been created."""
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='good_idx';")
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "Index 'good_idx' was not created in the database."

def test_triangles_csv_content():
    """Test that the triangles.csv file contains the correct output."""
    assert os.path.isfile(CSV_PATH), f"CSV file {CSV_PATH} is missing."

    with open(CSV_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 1, "CSV file is empty."
    assert lines[0] == "node1,node2,node3", f"CSV header is incorrect. Expected 'node1,node2,node3', got '{lines[0]}'."

    # Expected rows
    expected_rows = ["A,B,C", "X,Y,Z"]
    actual_rows = lines[1:]

    assert actual_rows == expected_rows, f"CSV content is incorrect. Expected {expected_rows}, got {actual_rows}."