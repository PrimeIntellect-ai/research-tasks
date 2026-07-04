# test_final_state.py

import os
import sqlite3
import csv
import pytest

DB_PATH = "/home/user/configs.db"
CSV_PATH = "/home/user/final_averages.csv"

def test_database_exists_and_schema():
    """Test that the SQLite database exists and has the correct schema."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table 'metrics' exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metrics'")
    table = cursor.fetchone()
    assert table is not None, "Table 'metrics' does not exist in the database."

    # Check schema
    cursor.execute("PRAGMA table_info(metrics)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}

    expected_columns = {
        'server_id': 'TEXT',
        'timestamp': 'INTEGER',
        'temp_celsius': 'REAL',
        'cpu_load': 'REAL'
    }

    for col, col_type in expected_columns.items():
        assert col in columns, f"Column '{col}' is missing from 'metrics' table."
        # SQLite types can be flexible, so we just check the column names exist.
        # But we can also check if the type is somewhat matching if provided.
        assert expected_columns[col] in columns[col].upper() or columns[col] == '', f"Column '{col}' has unexpected type {columns[col]}."

    conn.close()

def test_database_records():
    """Test that the database contains the correct interpolated and deduplicated records."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM metrics ORDER BY server_id, timestamp")
    rows = cursor.fetchall()

    # We expect 3 records for srv-A and 4 records for srv-B
    assert len(rows) == 7, f"Expected 7 records in the database, found {len(rows)}."

    records = [dict(row) for row in rows]

    # Check srv-A
    srv_a = [r for r in records if r['server_id'] == 'srv-A']
    assert len(srv_a) == 3, "Expected 3 records for srv-A."
    assert srv_a[0]['timestamp'] == 100 and srv_a[0]['temp_celsius'] == 40.0 and srv_a[0]['cpu_load'] == 10.0
    assert srv_a[1]['timestamp'] == 110 and srv_a[1]['temp_celsius'] == 45.0 and srv_a[1]['cpu_load'] == 15.0
    assert srv_a[2]['timestamp'] == 120 and srv_a[2]['temp_celsius'] == 50.0 and srv_a[2]['cpu_load'] == 20.0

    # Check srv-B
    srv_b = [r for r in records if r['server_id'] == 'srv-B']
    assert len(srv_b) == 4, "Expected 4 records for srv-B."
    assert srv_b[0]['timestamp'] == 100 and srv_b[0]['temp_celsius'] == 60.0 and srv_b[0]['cpu_load'] == 30.0
    assert srv_b[1]['timestamp'] == 110 and srv_b[1]['temp_celsius'] == 60.0 and srv_b[1]['cpu_load'] == 30.0
    assert srv_b[2]['timestamp'] == 120 and srv_b[2]['temp_celsius'] == 70.0 and srv_b[2]['cpu_load'] == 40.0
    assert srv_b[3]['timestamp'] == 130 and srv_b[3]['temp_celsius'] == 70.0 and srv_b[3]['cpu_load'] == 40.0

    conn.close()

def test_csv_export():
    """Test that the final_averages.csv file exists and contains the correct averages."""
    assert os.path.exists(CSV_PATH), f"CSV file {CSV_PATH} is missing."

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert reader.fieldnames == ['server_id', 'avg_temp', 'avg_load'], f"Unexpected CSV headers: {reader.fieldnames}"
    assert len(rows) == 2, f"Expected 2 rows in CSV, found {len(rows)}."

    data = {row['server_id']: row for row in rows}

    assert 'srv-A' in data, "srv-A missing from CSV."
    assert 'srv-B' in data, "srv-B missing from CSV."

    assert float(data['srv-A']['avg_temp']) == 45.0, f"srv-A avg_temp incorrect: {data['srv-A']['avg_temp']}"
    assert float(data['srv-A']['avg_load']) == 15.0, f"srv-A avg_load incorrect: {data['srv-A']['avg_load']}"

    assert float(data['srv-B']['avg_temp']) == 65.0, f"srv-B avg_temp incorrect: {data['srv-B']['avg_temp']}"
    assert float(data['srv-B']['avg_load']) == 35.0, f"srv-B avg_load incorrect: {data['srv-B']['avg_load']}"