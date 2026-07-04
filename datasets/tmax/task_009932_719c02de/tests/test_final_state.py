# test_final_state.py

import os
import sqlite3
import pytest

def test_c_file_exists():
    file_path = "/home/user/process_telemetry.c"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_tsv_file_contents():
    file_path = "/home/user/cleaned_telemetry.tsv"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    expected_lines = [
        "100\t20.00\tSystem Boot",
        "101\t21.00\tFILLED",
        "102\t22.00\tFILLED",
        "103\t23.00\tWarning: High Temp Detected",
        "104\t24.50\tOK",
        "105\t24.00\tFILLED",
        "106\t23.50\tFILLED",
        "107\t23.00\tFILLED",
        "108\t22.50\tCooling Down"
    ]

    with open(file_path, "r") as f:
        lines = [line.strip("\n") for line in f.readlines() if line.strip("\n")]

    assert lines == expected_lines, f"Contents of {file_path} do not match the expected output."

def test_sqlite_db_contents():
    db_path = "/home/user/telemetry.db"
    assert os.path.exists(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sensor_log';")
    assert cursor.fetchone() is not None, "Table 'sensor_log' does not exist in the database."

    # Check total count
    cursor.execute("SELECT count(*) FROM sensor_log;")
    count = cursor.fetchone()[0]
    assert count == 9, f"Expected 9 rows in sensor_log, found {count}."

    # Check interpolated row
    cursor.execute("SELECT temperature, status FROM sensor_log WHERE timestamp = 106;")
    row = cursor.fetchone()
    assert row is not None, "Missing row for timestamp 106."
    assert abs(row[0] - 23.5) < 0.01, f"Expected temperature 23.5 for timestamp 106, got {row[0]}."
    assert row[1] == "FILLED", f"Expected status 'FILLED' for timestamp 106, got '{row[1]}'."

    # Check cleaned row
    cursor.execute("SELECT status FROM sensor_log WHERE timestamp = 103;")
    row = cursor.fetchone()
    assert row is not None, "Missing row for timestamp 103."
    assert row[0] == "Warning: High Temp Detected", f"Expected cleaned status 'Warning: High Temp Detected' for timestamp 103, got '{row[0]}'."

    conn.close()