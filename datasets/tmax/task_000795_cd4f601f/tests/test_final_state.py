# test_final_state.py
import os
import sqlite3
import csv

def test_shortest_path_result():
    path_file = "/home/user/dataset/shortest_path.txt"
    assert os.path.isfile(path_file), f"File {path_file} does not exist."
    with open(path_file, "r") as f:
        content = f.read().strip()
    assert content == "10,25,40,88,99", f"Expected shortest path '10,25,40,88,99', got '{content}'"

def test_database_exists_and_schema():
    db_path = "/home/user/dataset/graph.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='citations'")
    assert cursor.fetchone() is not None, "Table 'citations' does not exist in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(citations)")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}
    assert 'source' in columns, "Column 'source' missing from 'citations' table."
    assert 'target' in columns, "Column 'target' missing from 'citations' table."
    assert 'INT' in columns['source'], "Column 'source' should be of type INTEGER."
    assert 'INT' in columns['target'], "Column 'target' should be of type INTEGER."

    # Check index
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='citations'")
    indices = cursor.fetchall()
    # Filter out auto-generated indices for sqlite internals if any, though usually explicit indices are what's created
    user_indices = [idx[0] for idx in indices if not idx[0].startswith('sqlite_autoindex')]
    assert len(user_indices) > 0, "No explicit index found on 'citations' table. An index was required."

    conn.close()

def test_database_content():
    db_path = "/home/user/dataset/graph.db"
    csv_path = "/home/user/dataset/citations.csv"

    if not os.path.isfile(db_path) or not os.path.isfile(csv_path):
        return # Handled by other tests

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader, None) # skip header
        csv_rows = list(reader)
        csv_count = len(csv_rows)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT count(*) FROM citations")
        db_count = cursor.fetchone()[0]
    except sqlite3.OperationalError:
        db_count = -1
    finally:
        conn.close()

    assert db_count == csv_count, f"Expected {csv_count} rows in database matching the CSV, got {db_count}."