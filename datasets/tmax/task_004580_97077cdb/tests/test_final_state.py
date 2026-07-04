# test_final_state.py
import os
import sqlite3
import csv

def test_index_dropped():
    db_path = '/home/user/etl_source.db'
    assert os.path.exists(db_path), f"Database file missing at {db_path}"

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_stale_data';")
    index = c.fetchone()
    conn.close()

    assert index is None, "The inefficient index 'idx_stale_data' was not dropped from the database."

def test_csv_output():
    csv_path = '/home/user/graph_in_degrees.csv'
    assert os.path.exists(csv_path), f"Output CSV file missing at {csv_path}"

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    expected_rows = [
        ['node', 'in_degree'],
        ['A', '1'],
        ['B', '2'],
        ['C', '2'],
        ['D', '1']
    ]

    assert rows == expected_rows, f"CSV content does not match expected output. Got: {rows}"