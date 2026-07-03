# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = '/home/user/metrics.db'

def test_db_exists():
    assert os.path.isfile(DB_PATH), f"The database file {DB_PATH} was not created."

def test_table_exists():
    assert os.path.isfile(DB_PATH), "Database missing, cannot check for table."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hourly_metrics';")
    table = cursor.fetchone()
    conn.close()
    assert table is not None, "The table 'hourly_metrics' does not exist in the database."

def test_table_schema():
    assert os.path.isfile(DB_PATH), "Database missing, cannot check schema."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(hourly_metrics);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}
    conn.close()

    expected_columns = {
        'bucket_hour': 'TEXT',
        'ip_address': 'TEXT',
        'avg_cpu': 'REAL',
        'max_mem': 'INTEGER'
    }

    for col_name, col_type in expected_columns.items():
        assert col_name in columns, f"Column '{col_name}' is missing from 'hourly_metrics'."
        # SQLite types can sometimes be flexible, but we check if it starts with the expected type or is exactly it
        assert columns[col_name].startswith(col_type), f"Column '{col_name}' has incorrect type. Expected {col_type}, got {columns[col_name]}."

def test_table_contents():
    assert os.path.isfile(DB_PATH), "Database missing, cannot check contents."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT bucket_hour, ip_address, avg_cpu, max_mem FROM hourly_metrics ORDER BY bucket_hour ASC, ip_address ASC;")
    rows = cursor.fetchall()
    conn.close()

    expected_rows = [
        ('2023-10-01 14:00:00', '192.168.1.10', 50.0, 2048),
        ('2023-10-01 15:00:00', '10.0.0.5', 85.0, 8192),
        ('2023-10-01 16:00:00', '192.168.1.10', 30.0, 512)
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in 'hourly_metrics', but found {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
        assert actual[0] == expected[0], f"Row {i+1}: Expected bucket_hour {expected[0]}, got {actual[0]}."
        assert actual[1] == expected[1], f"Row {i+1}: Expected ip_address {expected[1]}, got {actual[1]}."
        assert abs(actual[2] - expected[2]) < 1e-5, f"Row {i+1}: Expected avg_cpu {expected[2]}, got {actual[2]}."
        assert actual[3] == expected[3], f"Row {i+1}: Expected max_mem {expected[3]}, got {actual[3]}."