# test_final_state.py
import os
import sqlite3
import csv
import pytest

DB_PATH = '/home/user/backups.db'
CSV_PATH = '/home/user/anomalies.csv'

def test_database_exists_and_schema():
    """Test that the SQLite database and required table exist."""
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='backup_history';")
    table = cursor.fetchone()
    conn.close()

    assert table is not None, "Table 'backup_history' does not exist in the database."

def test_database_content():
    """Test that the database contains only the valid rows."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT backup_id, timestamp, status, size_bytes, database_name FROM backup_history ORDER BY backup_id")
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) == 12, f"Expected exactly 12 valid rows in backup_history, found {len(rows)}."

    backup_ids = {row['backup_id'] for row in rows}
    assert 'b_inv' not in backup_ids, "Invalid row 'b_inv' (string size_bytes) was not filtered out."

    # Check a sample valid row
    b1 = next((r for r in rows if r['backup_id'] == 'b1'), None)
    assert b1 is not None, "Missing backup_id 'b1'"
    assert b1['size_bytes'] == 100
    assert b1['status'] == 'SUCCESS'
    assert b1['database_name'] == 'DB_ALPHA'

def test_csv_exists_and_content():
    """Test that the anomalies CSV is generated correctly."""
    assert os.path.isfile(CSV_PATH), f"CSV file missing at {CSV_PATH}"

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."

    header = rows[0]
    expected_header = ['database_name', 'backup_id', 'spike_size']
    assert header == expected_header, f"CSV header mismatch. Expected {expected_header}, got {header}."

    data_rows = rows[1:]
    assert len(data_rows) == 2, f"Expected 2 anomaly rows, found {len(data_rows)}."

    # Check sorting
    db_names = [r[0] for r in data_rows]
    assert db_names == sorted(db_names), "CSV rows are not sorted alphabetically by database_name."

    # Check specific values
    expected_data = [
        ['DB_ALPHA', 'b4', '392.5'],
        ['DB_BETA', 'b9', '12.5']
    ]

    assert data_rows == expected_data, f"CSV data mismatch. Expected {expected_data}, got {data_rows}."