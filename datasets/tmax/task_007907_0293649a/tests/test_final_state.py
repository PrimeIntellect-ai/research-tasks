# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = '/home/user/logs/anomalies.db'

def test_database_exists():
    assert os.path.exists(DB_PATH), f"The database file {DB_PATH} was not found."
    assert os.path.isfile(DB_PATH), f"The path {DB_PATH} is not a file."

def test_database_schema_and_contents():
    assert os.path.exists(DB_PATH), f"Cannot check contents, {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='flagged_logs';")
    table_exists = cursor.fetchone()
    assert table_exists is not None, "The table 'flagged_logs' does not exist in the database."

    # Query the data
    cursor.execute("SELECT timestamp, endpoint, status_code, response_time_ms, rolling_avg FROM flagged_logs ORDER BY timestamp;")
    rows = cursor.fetchall()

    assert len(rows) == 2, f"Expected exactly 2 anomalous records in the database, but found {len(rows)}."

    # Expected rows
    # 107|/api/v1/users|500|150.0|71.2
    # 203|/api/v2/items|503|40.0|20.67

    row1 = rows[0]
    assert row1[0] == 107, f"Expected timestamp 107 for the first anomaly, got {row1[0]}."
    assert row1[1] == "/api/v1/users", f"Expected endpoint '/api/v1/users' for the first anomaly, got {row1[1]}."
    assert row1[2] == 500, f"Expected status_code 500 for the first anomaly, got {row1[2]}."
    assert float(row1[3]) == 150.0, f"Expected response_time_ms 150.0 for the first anomaly, got {row1[3]}."
    assert abs(float(row1[4]) - 71.2) < 0.01, f"Expected rolling_avg ~71.20 for the first anomaly, got {row1[4]}."

    row2 = rows[1]
    assert row2[0] == 203, f"Expected timestamp 203 for the second anomaly, got {row2[0]}."
    assert row2[1] == "/api/v2/items", f"Expected endpoint '/api/v2/items' for the second anomaly, got {row2[1]}."
    assert row2[2] == 503, f"Expected status_code 503 for the second anomaly, got {row2[2]}."
    assert float(row2[3]) == 40.0, f"Expected response_time_ms 40.0 for the second anomaly, got {row2[3]}."
    assert abs(float(row2[4]) - 20.67) < 0.01, f"Expected rolling_avg ~20.67 for the second anomaly, got {row2[4]}."

    conn.close()