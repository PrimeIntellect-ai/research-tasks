# test_final_state.py
import os
import csv
import sqlite3
import pytest

DB_PATH = '/home/user/config_history.db'
CSV_PATH = '/home/user/config_summary.csv'

def test_database_exists():
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"

def test_database_schema_and_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='server_configs'")
    assert cursor.fetchone() is not None, "Table 'server_configs' does not exist in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(server_configs)")
    columns = [row[1] for row in cursor.fetchall()]
    expected_columns = [
        'server_id',
        'timestamp',
        'hardware_ram_gb',
        'hardware_cpu_cores',
        'software_os',
        'software_is_active'
    ]

    for col in expected_columns:
        assert col in columns, f"Column '{col}' is missing from 'server_configs' table."

    # Check row count
    cursor.execute("SELECT COUNT(*) FROM server_configs")
    count = cursor.fetchone()[0]
    assert count == 6, f"Expected 6 rows in 'server_configs', but found {count}."

    # Check data normalization for boolean
    cursor.execute("SELECT software_is_active FROM server_configs WHERE software_is_active NOT IN (0, 1)")
    invalid_booleans = cursor.fetchall()
    assert len(invalid_booleans) == 0, f"Found invalid values for 'software_is_active': {invalid_booleans}. Expected 0 or 1."

    conn.close()

def test_csv_exists_and_content():
    assert os.path.isfile(CSV_PATH), f"CSV file missing at {CSV_PATH}"

    expected_csv = [
        ['server_id', 'snapshot_count', 'max_ram_gb', 'active_snapshots'],
        ['srv-alpha', '3', '32', '2'],
        ['srv-beta', '2', '8', '0'],
        ['srv-gamma', '1', '64', '1']
    ]

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_csv = list(reader)

    assert actual_csv == expected_csv, f"CSV content does not match expected output.\nExpected: {expected_csv}\nActual: {actual_csv}"