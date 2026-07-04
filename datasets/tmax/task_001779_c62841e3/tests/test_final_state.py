# test_final_state.py

import os
import sqlite3
import csv
import pytest

CSV_PATH = "/home/user/processed_logs.csv"
DB_PATH = "/home/user/logs.db"

def test_files_exist():
    assert os.path.isfile(CSV_PATH), f"The processed CSV file {CSV_PATH} is missing."
    assert os.path.isfile(DB_PATH), f"The SQLite database file {DB_PATH} is missing."

def test_csv_format_and_content():
    # Read the CSV to ensure it has the correct number of lines and columns
    # We use csv reader to handle commas inside the JSON payload correctly if they were quoted,
    # but the instructions say "comma-separated, no headers" and JSON is the last column.
    # The simplest way to parse it is to split by comma with maxsplit=6.

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 7, f"Expected 7 rows in the CSV, but found {len(lines)}."

    for i, line in enumerate(lines):
        parts = line.split(",", 6)
        assert len(parts) == 7, f"Row {i+1} in CSV does not have exactly 7 columns: {line}"

        # Check that the last column is valid JSON (starts with { and ends with })
        payload = parts[6].strip()
        assert payload.startswith("{") and payload.endswith("}"), f"Row {i+1} payload does not look like valid JSON: {payload}"

def test_database_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(metrics);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    expected_columns = {
        "timestamp": "TEXT",
        "ip": "TEXT",
        "endpoint": "TEXT",
        "status": "INTEGER",
        "response_time": "INTEGER",
        "rolling_avg": "INTEGER",
        "payload": "TEXT"
    }

    for col, ctype in expected_columns.items():
        assert col in columns, f"Column '{col}' is missing from the 'metrics' table."
        # SQLite types can be flexible, but we check if it's broadly correct or just exists
        assert ctype in columns[col] or columns[col] == "", f"Column '{col}' should be of type {ctype}, found {columns[col]}."

    conn.close()

def test_database_row_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM metrics;")
    count = cursor.fetchone()[0]

    assert count == 7, f"Expected 7 rows in the 'metrics' table, but found {count}."

    conn.close()

def test_database_rolling_averages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check /api/v1/users
    cursor.execute("SELECT rolling_avg FROM metrics WHERE endpoint='/api/v1/users' ORDER BY timestamp;")
    users_avg = [row[0] for row in cursor.fetchall()]
    expected_users_avg = [150, 175, 200, 250, 216]
    assert users_avg == expected_users_avg, f"Rolling averages for /api/v1/users are incorrect. Expected {expected_users_avg}, got {users_avg}."

    # Check /api/v1/data
    cursor.execute("SELECT rolling_avg FROM metrics WHERE endpoint='/api/v1/data' ORDER BY timestamp;")
    data_avg = [row[0] for row in cursor.fetchall()]
    expected_data_avg = [300, 350]
    assert data_avg == expected_data_avg, f"Rolling averages for /api/v1/data are incorrect. Expected {expected_data_avg}, got {data_avg}."

    conn.close()

def test_database_deduplication_and_filtering():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check that negative response times are filtered out
    cursor.execute("SELECT COUNT(*) FROM metrics WHERE response_time < 0;")
    negative_count = cursor.fetchone()[0]
    assert negative_count == 0, "Found rows with negative response_time, which should have been filtered out."

    # Check that duplicates are removed
    cursor.execute("SELECT ip, endpoint, payload, COUNT(*) FROM metrics GROUP BY ip, endpoint, payload HAVING COUNT(*) > 1;")
    duplicates = cursor.fetchall()
    assert len(duplicates) == 0, f"Found duplicate entries based on IP, ENDPOINT, and PAYLOAD: {duplicates}"

    conn.close()