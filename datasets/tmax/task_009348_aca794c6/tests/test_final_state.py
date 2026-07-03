# test_final_state.py

import os
import sqlite3
import hashlib
import pytest

DB_PATH = "/home/user/errors.db"
LOG_PATH = "/home/user/raw_server_logs.txt"

def get_expected_data():
    """
    Computes the expected database rows directly from the raw_server_logs.txt
    file, mimicking the filtering, alignment, and hashing logic.
    """
    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} is missing."

    seen_hashes = set()
    expected_rows = []

    with open(LOG_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "ERROR:" not in line:
                continue

            # Example line: [2023-10-25 14:32:45.123] ERROR: Connection timeout - ID:usr_123
            # Extract parts
            try:
                timestamp_part, rest = line.split("] ", 1)
                timestamp_full = timestamp_part.lstrip("[")

                # Align to minute: 2023-10-25 14:32:45.123 -> 2023-10-25 14:32:00
                date_time, ms = timestamp_full.split(".")
                date, time = date_time.split(" ")
                hour, minute, sec = time.split(":")
                aligned_timestamp = f"{date} {hour}:{minute}:00"

                level_msg, user_part = rest.split(" - ID:")
                message = level_msg.replace("ERROR: ", "").strip()
                user_id = user_part.strip()

                hash_input = f"{aligned_timestamp}|{message}|{user_id}"
                hash_id = hashlib.md5(hash_input.encode('utf-8')).hexdigest()

                if hash_id not in seen_hashes:
                    seen_hashes.add(hash_id)
                    expected_rows.append((hash_id, aligned_timestamp, message, user_id))
            except Exception as e:
                pytest.fail(f"Failed to parse log line for expected truth: {line}. Error: {e}")

    # Sort to ensure consistent comparison
    expected_rows.sort(key=lambda x: (x[1], x[0]))
    return expected_rows


def test_db_exists():
    assert os.path.isfile(DB_PATH), f"The database file {DB_PATH} was not created."

def test_db_schema():
    assert os.path.isfile(DB_PATH), f"The database file {DB_PATH} was not created."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='error_logs';")
    table = cursor.fetchone()
    assert table is not None, "Table 'error_logs' does not exist in the database."

    # Check schema
    cursor.execute("PRAGMA table_info(error_logs);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    expected_columns = {
        "hash_id": "TEXT",
        "timestamp": "TEXT",
        "message": "TEXT",
        "user_id": "TEXT"
    }

    for col, col_type in expected_columns.items():
        assert col in columns, f"Column '{col}' is missing from 'error_logs' table."
        # SQLite types can sometimes be flexible, but we check if TEXT is in the defined type
        assert "TEXT" in columns[col], f"Column '{col}' should be of type TEXT, but is {columns[col]}."

    conn.close()

def test_db_content():
    assert os.path.isfile(DB_PATH), f"The database file {DB_PATH} was not created."

    expected_rows = get_expected_data()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT hash_id, timestamp, message, user_id FROM error_logs ORDER BY timestamp ASC, hash_id ASC;")
    actual_rows = cursor.fetchall()
    conn.close()

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch.\nExpected: {expected}\nActual: {actual}"