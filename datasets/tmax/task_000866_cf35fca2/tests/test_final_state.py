# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/features.db"

def test_database_exists():
    """Check if the SQLite database was created."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    assert os.path.isfile(DB_PATH), f"Path {DB_PATH} is not a file"

def test_table_schema_and_contents():
    """Check the schema and contents of the sensor_stats table."""
    assert os.path.exists(DB_PATH), "Database missing"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sensor_stats';")
    table = cursor.fetchone()
    assert table is not None, "Table 'sensor_stats' does not exist in the database."

    # Fetch all rows
    cursor.execute("SELECT sensor_id, n_deltas, is_drifting FROM sensor_stats ORDER BY sensor_id;")
    rows = cursor.fetchall()

    assert len(rows) == 10, f"Expected 10 rows in sensor_stats, found {len(rows)}"

    expected_drifting = {3, 7}

    for row in rows:
        sensor_id, n_deltas, is_drifting = row

        # Check n_deltas bounds (approx 950, since 5% corrupted out of 1000 records, minus 1 for first valid)
        assert 900 <= n_deltas <= 1000, f"Sensor {sensor_id} has unexpected n_deltas: {n_deltas}"

        # Check drifting flag
        if sensor_id in expected_drifting:
            assert is_drifting == 1, f"Sensor {sensor_id} should be drifting (is_drifting=1), but got {is_drifting}"
        else:
            assert is_drifting == 0, f"Sensor {sensor_id} should NOT be drifting (is_drifting=0), but got {is_drifting}"

    conn.close()