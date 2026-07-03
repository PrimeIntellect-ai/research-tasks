# test_final_state.py

import os
import sqlite3
import pytest

def test_c_source_and_executable_exist():
    source_path = "/home/user/cleaner.c"
    exec_path = "/home/user/cleaner"

    assert os.path.isfile(source_path), f"C source file missing at {source_path}"
    assert os.path.isfile(exec_path), f"Executable missing at {exec_path}"
    assert os.access(exec_path, os.X_OK), f"Executable at {exec_path} is not executable"

def test_clean_sensors_csv_content():
    csv_path = "/home/user/clean_sensors.csv"
    assert os.path.isfile(csv_path), f"Cleaned CSV missing at {csv_path}"

    expected_lines = [
        "100,50.50,Tokyo, Japan Zone A,50.50",
        "101,50.50,Tokyo, Japan Zone A,50.50",
        "102,50.50,Tokyo, Japan Zone A,50.50",
        "103,60.50,Paris, France,53.83",
        "104,60.50,Paris, France,57.17",
        "105,70.50,São Paulo, Brazil,63.83"
    ]

    with open(csv_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows, found {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at row {i+1}. Expected: '{expected}', Got: '{actual}'"

def test_sqlite_db_content():
    db_path = "/home/user/sensors.db"
    assert os.path.isfile(db_path), f"SQLite database missing at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cleaned_readings';")
    assert cursor.fetchone() is not None, "Table 'cleaned_readings' does not exist in the database."

    # Check schema and data
    cursor.execute("SELECT timestamp, sensor_value, location_desc, ma_3 FROM cleaned_readings ORDER BY timestamp ASC;")
    rows = cursor.fetchall()

    expected_data = [
        (100, 50.50, "Tokyo, Japan Zone A", 50.50),
        (101, 50.50, "Tokyo, Japan Zone A", 50.50),
        (102, 50.50, "Tokyo, Japan Zone A", 50.50),
        (103, 60.50, "Paris, France", 53.83),
        (104, 60.50, "Paris, France", 57.17),
        (105, 70.50, "São Paulo, Brazil", 63.83)
    ]

    assert len(rows) == len(expected_data), f"Expected {len(expected_data)} rows in database, found {len(rows)}"

    for i, (actual, expected) in enumerate(zip(rows, expected_data)):
        assert actual[0] == expected[0], f"Row {i+1} timestamp mismatch: expected {expected[0]}, got {actual[0]}"
        assert abs(actual[1] - expected[1]) < 0.01, f"Row {i+1} sensor_value mismatch: expected {expected[1]}, got {actual[1]}"
        assert actual[2] == expected[2], f"Row {i+1} location_desc mismatch: expected '{expected[2]}', got '{actual[2]}'"
        assert abs(actual[3] - expected[3]) < 0.01, f"Row {i+1} ma_3 mismatch: expected {expected[3]}, got {actual[3]}"

    conn.close()