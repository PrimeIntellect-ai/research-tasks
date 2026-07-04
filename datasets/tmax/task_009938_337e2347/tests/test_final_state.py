# test_final_state.py
import os
import sqlite3
import pytest

def test_clean_sensors_exists_and_utf8():
    file_path = "/home/user/clean_sensors.csv"
    assert os.path.exists(file_path), f"The file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        assert len(lines) > 0, f"The file {file_path} is empty."

        # Check for missing values (empty strings between commas or at the end)
        for i, line in enumerate(lines):
            parts = line.strip().split(",")
            assert len(parts) == 4, f"Line {i+1} does not have exactly 4 columns: {line}"
            assert parts[3] != "", f"Line {i+1} has a missing reading value: {line}"

    except UnicodeDecodeError:
        pytest.fail(f"The file {file_path} is not properly UTF-8 encoded.")

def test_database_and_table_schema():
    db_path = "/home/user/sensor_data.db"
    assert os.path.exists(db_path), f"The database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table 'readings' exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings';")
    assert cursor.fetchone() is not None, "Table 'readings' does not exist in the database."

    # Check schema
    cursor.execute("PRAGMA table_info(readings);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    assert "seq_id" in columns, "Column 'seq_id' is missing."
    assert "timestamp" in columns, "Column 'timestamp' is missing."
    assert "location_name" in columns, "Column 'location_name' is missing."
    assert "reading" in columns, "Column 'reading' is missing."

    conn.close()

def test_database_data_and_interpolation():
    db_path = "/home/user/sensor_data.db"
    assert os.path.exists(db_path), f"The database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if data was imported
    cursor.execute("SELECT COUNT(*) FROM readings;")
    count = cursor.fetchone()[0]
    assert count > 0, "Table 'readings' is empty."

    # Check specific interpolated values based on the setup data
    # seq_id 2 should be 15.0
    cursor.execute("SELECT reading FROM readings WHERE seq_id = 2;")
    row = cursor.fetchone()
    if row:
        assert abs(float(row[0]) - 15.0) < 0.01, f"Interpolated value for seq_id 2 is incorrect. Expected 15.0, got {row[0]}"

    # seq_id 5 should be 23.5
    cursor.execute("SELECT reading FROM readings WHERE seq_id = 5;")
    row = cursor.fetchone()
    if row:
        assert abs(float(row[0]) - 23.5) < 0.01, f"Interpolated value for seq_id 5 is incorrect. Expected 23.5, got {row[0]}"

    # seq_id 8 should be 28.0
    cursor.execute("SELECT reading FROM readings WHERE seq_id = 8;")
    row = cursor.fetchone()
    if row:
        assert abs(float(row[0]) - 28.0) < 0.01, f"Interpolated value for seq_id 8 is incorrect. Expected 28.0, got {row[0]}"

    conn.close()

def test_verification_log():
    log_path = "/home/user/verification.log"
    assert os.path.exists(log_path), f"The file {log_path} does not exist."

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert "22.19" in content, f"The verification log does not contain the correct average '22.19'. Found: '{content}'"