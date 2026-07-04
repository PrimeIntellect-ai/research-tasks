# test_final_state.py

import os
import csv
import sqlite3
import pytest

CSV_PATH = "/home/user/aggregated.csv"
DB_PATH = "/home/user/sensor_data.db"

def test_csv_exists_and_content():
    assert os.path.exists(CSV_PATH), f"CSV file {CSV_PATH} is missing."
    assert os.path.isfile(CSV_PATH), f"Path {CSV_PATH} is not a file."

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."

    header = rows[0]
    assert header == ['sensor_name', 'bucket_time', 'avg_value'], f"Incorrect CSV header: {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected 3 data rows, got {len(data_rows)}."

    # Row 1
    assert data_rows[0][0] == 'humidity_b', f"Row 1 sensor_name wrong: {data_rows[0][0]}"
    assert data_rows[0][1] == '1672574400', f"Row 1 bucket_time wrong: {data_rows[0][1]}"
    assert float(data_rows[0][2]) == 45.0, f"Row 1 avg_value wrong: {data_rows[0][2]}"

    # Row 2
    assert data_rows[1][0] == 'temp_a', f"Row 2 sensor_name wrong: {data_rows[1][0]}"
    assert data_rows[1][1] == '1672574400', f"Row 2 bucket_time wrong: {data_rows[1][1]}"
    assert float(data_rows[1][2]) == 23.5, f"Row 2 avg_value wrong: {data_rows[1][2]}"

    # Row 3
    assert data_rows[2][0] == 'temp_a', f"Row 3 sensor_name wrong: {data_rows[2][0]}"
    assert data_rows[2][1] == '1672578000', f"Row 3 bucket_time wrong: {data_rows[2][1]}"
    assert float(data_rows[2][2]) == 25.0, f"Row 3 avg_value wrong: {data_rows[2][2]}"

def test_sqlite_db_exists_and_content():
    assert os.path.exists(DB_PATH), f"SQLite database {DB_PATH} is missing."
    assert os.path.isfile(DB_PATH), f"Path {DB_PATH} is not a file."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hourly_aggregates'")
    table = cursor.fetchone()
    assert table is not None, "Table 'hourly_aggregates' does not exist in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(hourly_aggregates)")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    assert 'sensor_name' in columns, "Column 'sensor_name' missing."
    assert 'TEXT' in columns['sensor_name'], f"Column 'sensor_name' should be TEXT, got {columns['sensor_name']}."

    assert 'bucket_time' in columns, "Column 'bucket_time' missing."
    assert 'INT' in columns['bucket_time'], f"Column 'bucket_time' should be INTEGER, got {columns['bucket_time']}."

    assert 'avg_value' in columns, "Column 'avg_value' missing."
    assert 'REAL' in columns['avg_value'] or 'NUM' in columns['avg_value'] or 'FLOAT' in columns['avg_value'], f"Column 'avg_value' should be REAL, got {columns['avg_value']}."

    # Check data
    cursor.execute("SELECT sensor_name, bucket_time, avg_value FROM hourly_aggregates ORDER BY sensor_name ASC, bucket_time ASC")
    db_rows = cursor.fetchall()
    conn.close()

    assert len(db_rows) == 3, f"Expected 3 rows in database, got {len(db_rows)}."

    assert db_rows[0][0] == 'humidity_b'
    assert int(db_rows[0][1]) == 1672574400
    assert float(db_rows[0][2]) == 45.0

    assert db_rows[1][0] == 'temp_a'
    assert int(db_rows[1][1]) == 1672574400
    assert float(db_rows[1][2]) == 23.5

    assert db_rows[2][0] == 'temp_a'
    assert int(db_rows[2][1]) == 1672578000
    assert float(db_rows[2][2]) == 25.0