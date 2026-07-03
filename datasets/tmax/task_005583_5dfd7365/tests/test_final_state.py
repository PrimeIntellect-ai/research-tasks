# test_final_state.py

import os
import sqlite3
import pytest

def test_files_exist():
    """Verify that all expected files exist."""
    expected_files = [
        "/home/user/process.c",
        "/home/user/Makefile",
        "/home/user/processor",
        "/home/user/sorted_data.csv",
        "/home/user/anomalies.csv",
        "/home/user/sensor_db.sqlite"
    ]
    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Missing expected file: {file_path}"

def test_sorted_data_csv_content():
    """Verify the contents of sorted_data.csv."""
    expected_lines = [
        "1,100,12.00",
        "1,105,10.00",
        "1,110,35.00",
        "2,100,45.00",
        "2,101,46.00",
        "2,102,80.00",
        "3,500,10.00",
        "3,501,15.00"
    ]
    with open("/home/user/sorted_data.csv", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, "sorted_data.csv content is incorrect."

def test_anomalies_csv_content():
    """Verify the contents of anomalies.csv."""
    expected_lines = [
        "1,110,35.00,10.00",
        "2,102,80.00,46.00"
    ]
    with open("/home/user/anomalies.csv", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, "anomalies.csv content is incorrect."

def test_sqlite_database_content():
    """Verify the schema and data in the SQLite database."""
    db_path = "/home/user/sensor_db.sqlite"
    assert os.path.isfile(db_path), "SQLite database not found."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check sensor_data table count
    cursor.execute("SELECT COUNT(*) FROM sensor_data;")
    sensor_data_count = cursor.fetchone()[0]
    assert sensor_data_count == 8, f"Expected 8 rows in sensor_data, got {sensor_data_count}"

    # Check anomalies table count
    cursor.execute("SELECT COUNT(*) FROM anomalies;")
    anomalies_count = cursor.fetchone()[0]
    assert anomalies_count == 2, f"Expected 2 rows in anomalies, got {anomalies_count}"

    # Check anomalies data
    cursor.execute("SELECT sensor_id, timestamp FROM anomalies ORDER BY sensor_id;")
    anomalies_data = cursor.fetchall()
    expected_anomalies = [(1, 110), (2, 102)]
    assert anomalies_data == expected_anomalies, f"Expected anomalies data {expected_anomalies}, got {anomalies_data}"

    conn.close()

def test_makefile_contains_targets():
    """Verify the Makefile contains the required targets."""
    with open("/home/user/Makefile", "r") as f:
        content = f.read()

    for target in ["build", "process", "load", "all"]:
        assert f"{target}:" in content, f"Makefile is missing target: {target}"