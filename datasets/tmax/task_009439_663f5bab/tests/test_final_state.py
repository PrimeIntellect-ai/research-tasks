# test_final_state.py

import os
import sqlite3
import stat
import pytest

DB_PATH = "/home/user/sensor_data.db"
SCRIPT_PATH = "/home/user/detect_anomalies.sh"
ANOMALIES_PATH = "/home/user/anomalies.csv"

def test_database_exists_and_schema():
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} is missing."
    assert os.path.isfile(DB_PATH), f"{DB_PATH} is not a file."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings';")
    assert cursor.fetchone() is not None, "Table 'readings' does not exist in the database."

    # Check schema
    cursor.execute("PRAGMA table_info(readings);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    assert "timestamp" in columns and columns["timestamp"] == "TEXT", "Column 'timestamp' missing or not TEXT."
    assert "sensor_id" in columns and columns["sensor_id"] == "TEXT", "Column 'sensor_id' missing or not TEXT."
    assert "temperature" in columns and columns["temperature"] == "REAL", "Column 'temperature' missing or not REAL."

    conn.close()

def test_database_contents():
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM readings;")
        count = cursor.fetchone()[0]
        assert count == 8, f"Expected 8 rows in 'readings' table, found {count}."

        # Verify a sample of the data to ensure correct import
        cursor.execute("SELECT temperature FROM readings WHERE sensor_id='sensor_1' AND timestamp='2023-10-01T00:02:00Z';")
        temp = cursor.fetchone()
        assert temp is not None, "Expected reading for sensor_1 at 2023-10-01T00:02:00Z is missing."
        assert abs(temp[0] - 38.0) < 0.01, f"Expected temperature 38.0, found {temp[0]}."
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query the database: {e}")
    finally:
        conn.close()

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable by the owner."

def test_anomalies_csv():
    assert os.path.exists(ANOMALIES_PATH), f"Output file {ANOMALIES_PATH} is missing."
    assert os.path.isfile(ANOMALIES_PATH), f"{ANOMALIES_PATH} is not a file."

    with open(ANOMALIES_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "sensor_id,timestamp,temperature,previous_temperature",
        "sensor_1,2023-10-01T00:02:00Z,38.0,21.5",
        "sensor_2,2023-10-01T00:02:30Z,-5.0,14.0"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {ANOMALIES_PATH}, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual}'"