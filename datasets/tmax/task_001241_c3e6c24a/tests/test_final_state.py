# test_final_state.py

import os
import sqlite3
import socket
import time
import pytest

def test_recovered_database_row_count():
    db_path = "/home/user/recovered.db"
    assert os.path.isfile(db_path), f"Recovered database not found at {db_path}"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM telemetry;")
        count = cursor.fetchone()[0]
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to query the recovered database: {e}")

    assert count >= 4800, f"Recovered database has {count} rows, expected at least 4800."

def test_pipeline_end_to_end():
    db_path = "/home/user/app/data.db"
    assert os.path.isfile(db_path), f"Application database not found at {db_path}"

    # Send a normal record and a negative record (to trigger the fixed anomaly)
    test_records = [
        ("sensorX", 99.9),
        ("sensorY", -5.0)
    ]

    for sensor, value in test_records:
        payload = f"{sensor},{value}\n".encode('utf-8')
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect(("127.0.0.1", 8080))
            s.sendall(payload)
            s.close()
        except Exception as e:
            pytest.fail(f"Failed to send data to API server on port 8080: {e}")

    # Wait for the worker to process the spool file
    time.sleep(2)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for sensor, value in test_records:
            cursor.execute("SELECT count(*) FROM telemetry WHERE sensor = ? AND value = ?", (sensor, value))
            count = cursor.fetchone()[0]
            assert count > 0, f"Record for {sensor} with value {value} was not found in the database. Pipeline might be hanging or dropping data."

        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to query the application database: {e}")